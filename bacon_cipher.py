"""
Requires:
python-lorem
"""
import string

import lorem


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


class BaconCipher:

    def __init__(self, carrier_message=None):
        self.carrier_message = carrier_message
        if carrier_message is not None:
            self.carrier_message = carrier_message.lower()
        self.alphabet = string.ascii_uppercase

    def advance_carrier_index(self):
        skipped_chars = ""
        self.carrier_index += 1
        while self.carrier_message[self.carrier_index].upper() not in self.alphabet:
            skipped_chars += self.carrier_message[self.carrier_index]
            self.carrier_index += 1
        return skipped_chars

    def encrypt(self, plaintext):
        min_carrier_size = len(plaintext) * 5
        plaintext = plaintext.upper()

        cipher_text_list = []

        self.carrier_index = 0

        if self.carrier_message:
            if len(self.carrier_message) < min_carrier_size:
                raise ValueError("Carrier message is too short.")
        else:

            self.carrier_message = lorem.get_paragraph(count=min_carrier_size // 3)

            for letter in plaintext:
                letter_binary = format(self.alphabet.index(letter), "05b")

                for bin_char in letter_binary:
                    if bin_char == "0":
                        cipher_text_list.append(self.carrier_message[self.carrier_index].lower())
                    elif bin_char == "1":
                        cipher_text_list.append(self.carrier_message[self.carrier_index].upper())

                    skipped_chars = self.advance_carrier_index()
                    cipher_text_list.append(skipped_chars)

        return "".join(cipher_text_list)

    def decrypt(self, ciphertext):
        upper_alpha = string.ascii_uppercase
        lower_alpha = string.ascii_lowercase
        binary_list = []
        plain_text_list = []
        for letter in ciphertext:
            if letter in upper_alpha:
                binary_list.append("1")
            elif letter in lower_alpha:
                binary_list.append("0")
            else:
                # skip any non letters
                pass


        print()
        for chunk in list(divide_chunks(binary_list, 5)):
            chunk_str = "".join(chunk)
            index = int(chunk_str, 2)
            plain_text_list.append(self.alphabet[index])
        return "".join(plain_text_list)


if __name__ == '__main__':
    # print(lorem.get_paragraph(5))
    bacon_cipher = BaconCipher()
    ciphertext = bacon_cipher.encrypt("BACONCIPHER")
    print(ciphertext)

    print(bacon_cipher.decrypt(ciphertext))

