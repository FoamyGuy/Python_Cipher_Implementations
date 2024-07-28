import secrets
import random

class BookCipher:
    def __init__(self):
        self.swaps = {}
        self.force_uppercase = False

    @property
    def book_str(self):
        raise NotImplementedError

    def encrypt(self, plain_text):
        if self.force_uppercase:
            plain_text = plain_text.upper()
        cipher_text_list = []

        shuffled_letter_indexes = {}
        current_indexes = {}
        for index, letter in enumerate(self.book_str):
            if letter in shuffled_letter_indexes:
                if secrets.randbelow(2) == 0:
                    shuffled_letter_indexes[letter].append(index)
                else:
                    shuffled_letter_indexes[letter].insert(0, index)
            else:
                shuffled_letter_indexes[letter] = [index]

            current_indexes[letter] = 0

        for letter in plain_text:
            if letter in self.swaps:
                letter = self.swaps[letter]

            if letter in self.book_str:
                cipher_text_list.append(shuffled_letter_indexes[letter][current_indexes[letter]])
                current_indexes[letter] += 1
                if current_indexes[letter] >= len(shuffled_letter_indexes[letter]):
                    random.shuffle(shuffled_letter_indexes[letter])
                    current_indexes[letter] = 0

        return cipher_text_list

    def decrypt(self, cipher_text_list):
        plain_text_list = []
        for index in cipher_text_list:
            letter = self.book_str[index]
            if letter in self.swaps:
                letter = self.swaps[letter]
            plain_text_list.append(letter)
        return "".join(plain_text_list)