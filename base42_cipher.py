import secrets
import string


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def number_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def list_to_base_10(list_num, from_base):
    result = 0
    for index, digit in enumerate(reversed(list_num)):
        result += digit * (from_base ** index)

    return result


def digits_list_to_str(digits_list, alphabet):
    output_str_list = []
    for digit in digits_list:
        output_str_list.append(alphabet[digit])

    return "".join(output_str_list)


def str_to_digits_list(str_num, alphabet):
    digits_list = []
    for char in str_num:
        digits_list.append(alphabet.index(char))
    return digits_list


class Base42Cipher:
    DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP"
    DEFAULT_PADBYTE_INDICATOR = "="

    DECOY_ALL_LETTERS = 0
    DECOY_B64 = 1

    def __init__(self, alphabet=DEFAULT_ALPHABET, pad_byte_indicator=DEFAULT_PADBYTE_INDICATOR,
                 decoy_alphabet=None, decoy_factor=0):
        self.alphabet = alphabet
        self.pad_byte_indicator = pad_byte_indicator

        if isinstance(decoy_alphabet, str):
            self._decoy_alphabet = decoy_alphabet
        elif decoy_alphabet == Base42Cipher.DECOY_B64:
            self._decoy_alphabet = self.find_all_valid_b64_decoys()
        elif decoy_alphabet == Base42Cipher.DECOY_ALL_LETTERS:
            self._decoy_alphabet = self.find_all_valid_letter_decoys()
        else:
            raise ValueError("Invalid decoy_alphabet")

        if decoy_factor < 0 or decoy_factor > 100:
            raise ValueError("Invalid decoy_factor")

        self._decoy_factor = decoy_factor

        if pad_byte_indicator in self.alphabet:
            raise ValueError("Pad byte indicator must not be in alphabet")

    @property
    def decoy_factor(self):
        return self._decoy_factor

    @property
    def decoy_alphabet(self):
        return self._decoy_alphabet

    @decoy_alphabet.setter
    def decoy_alphabet(self, decoy_alphabet):
        self._decoy_alphabet = decoy_alphabet

    @decoy_factor.setter
    def decoy_factor(self, decoy_factor):
        self._decoy_factor = decoy_factor

    def encrypt(self, plaintext_bytes: bytes) -> str:
        ciphertext_list = []
        padded = False
        if len(plaintext_bytes) % 2 == 1:
            plaintext_bytes += b'\x00'
            padded = True

        for digram in divide_chunks(plaintext_bytes, 2):
            int_val = int.from_bytes(digram)
            base42_digits = number_to_base(int_val, 42)
            while len(base42_digits) < 3:
                base42_digits.insert(0, 0)

            ciphertext_list.append(digits_list_to_str(base42_digits, self.alphabet))
            decoy_roll = secrets.randbelow(100)
            #print(f"decoy_roll: {decoy_roll} | factor: {self.decoy_factor}")
            if self.decoy_factor and decoy_roll < self.decoy_factor:
                selected_decoy = self.decoy_alphabet[secrets.randbelow(len(self.decoy_alphabet))]
                #print(f"selected decoy: {selected_decoy}")
                ciphertext_list.append(selected_decoy)

        if padded:
            ciphertext_list.append(self.pad_byte_indicator)
        return "".join(ciphertext_list)

    def decrypt(self, ciphertext: str) -> bytes:
        clearbytes_digrams = []

        padded = False
        if ciphertext[-1] == self.pad_byte_indicator:
            ciphertext = ciphertext[:-1]
            padded = True

        cleaned_ciphertext = []
        for letter in ciphertext:
            if letter in self.alphabet:
                cleaned_ciphertext.append(letter)
        ciphertext = "".join(cleaned_ciphertext)

        for triplet in divide_chunks(ciphertext, 3):
            num_list = str_to_digits_list(triplet, self.alphabet)
            num_int = list_to_base_10(num_list, 42)
            clearbytes_digrams.append(num_int.to_bytes(2))

        if padded:
            clearbytes_digrams[-1] = clearbytes_digrams[-1][0].to_bytes(1)
        return b"".join(clearbytes_digrams)

    def find_all_valid_letter_decoys(self):
        valid_decoys = []
        for letter in string.ascii_letters:
            if letter not in self.alphabet and letter != self.pad_byte_indicator:
                valid_decoys.append(letter)
        return valid_decoys

    def find_all_valid_b64_decoys(self):
        valid_decoys = []
        b64_alphabet = string.ascii_letters + string.digits + "+/"
        for letter in b64_alphabet:
            if letter not in self.alphabet and letter != self.pad_byte_indicator:
                valid_decoys.append(letter)
        return valid_decoys

    @staticmethod
    def get_alphabet_from_passphrases(lowercase_passphrase, uppercase_passphrase):
        lowercase_passphrase = lowercase_passphrase.lower()
        uppercase_passphrase = uppercase_passphrase.upper()

        alphabet_list = []
        for letter in lowercase_passphrase:
            if letter not in alphabet_list:
                alphabet_list.append(letter)

        for letter in string.ascii_lowercase:
            if letter not in alphabet_list:
                alphabet_list.append(letter)

        for letter in uppercase_passphrase:
            # print(f"checking: {letter}")
            if letter not in alphabet_list:
                # print(f"{letter} wasn't in list")
                alphabet_list.append(letter)

        upper_index = 0
        while len(alphabet_list) < len(Base42Cipher.DEFAULT_ALPHABET):
            upper_letter = string.ascii_uppercase[upper_index]
            if upper_letter not in alphabet_list:
                alphabet_list.append(upper_letter)
            upper_index += 1

        return "".join(alphabet_list)


if __name__ == '__main__':
    # print(digits_list_to_str([0, 0, 0], Base42Cipher.DEFAULT_ALPHABET))

    #b42_default = Base42Cipher()

    # ciphertext = b42_default.encrypt(b"Hello World")
    # print(ciphertext)
    # print(b42_default.decrypt(ciphertext))

    # b42_custom = Base42Cipher(
    #     Base42Cipher.get_alphabet_from_passphrases(
    #         "first",
    #         "SECOND"
    #     )
    # )
    #
    # custom_ciphertext = b42_custom.encrypt(b"Hello World")
    # print(f"custom: {custom_ciphertext}")
    # print(f"custom: {b42_custom.decrypt(custom_ciphertext)}")



    b42_with_decoys = Base42Cipher(decoy_alphabet=Base42Cipher.DECOY_B64, decoy_factor=70)

    ciphertext = b42_with_decoys.encrypt(b"Hello World")

    print(ciphertext)

    print(b42_with_decoys.decrypt(ciphertext))
