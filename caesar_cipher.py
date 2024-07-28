import string


class CaesarCipher:
    ALPHABET = string.ascii_uppercase

    def __init__(self, shift):
        self.shift = shift

    def encrypt(self, plain_text):
        cipher_text_list = []
        for letter in plain_text.upper():
            if letter in self.ALPHABET:
                real_index = self.ALPHABET.index(letter)
                shifted_index = real_index + self.shift
                cipher_text_list.append(self.ALPHABET[shifted_index % len(self.ALPHABET)])
            if letter == ' ':
                cipher_text_list.append(' ')
        return ''.join(cipher_text_list)

    def decrypt(self, cipher_text):
        clear_text_list = []
        for letter in cipher_text:
            if letter in self.ALPHABET:
                shifted_index = self.ALPHABET.index(letter)
                real_index = shifted_index - self.shift
                clear_text_list.append(self.ALPHABET[real_index % len(self.ALPHABET)])
            else:
                clear_text_list.append(letter)
        return ''.join(clear_text_list)


if __name__ == '__main__':
    caeser = CaesarCipher(shift=5)
    cipher_text = caeser.encrypt('Hello World')
    print(cipher_text)

    clear_text = caeser.decrypt(cipher_text)
    print(clear_text)