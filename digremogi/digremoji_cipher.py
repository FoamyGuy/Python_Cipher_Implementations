import string

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
class DigremojiCipher:
    def __init__(self, emoji_alphabet=None):
        if emoji_alphabet is None:
            with open("digremoji_alphabet_with_spaces_shuffled_keep1.txt", "r") as f:
                self.emoji_alphabet = f.read()

        self.map = {}
        emoji_index = 0
        alphabet_with_space = string.ascii_uppercase + " "

        for first_letter in alphabet_with_space:
            for second_letter in alphabet_with_space:
                self.map[f"{first_letter}{second_letter}"] = self.emoji_alphabet[emoji_index]
                self.map[self.emoji_alphabet[emoji_index]] = f"{first_letter}{second_letter}"
                emoji_index += 1
        print(self.map)

    def encrypt(self, plain_text):
        #plain_text = plain_text.replace(" ", "").upper()
        plain_text = plain_text.upper()

        cipher_text_list = []
        if len(plain_text) % 2 == 1:
            plain_text += " "

        for digram in divide_chunks(plain_text, 2):
            cipher_text_list.append(self.map[digram])

        return "".join(cipher_text_list)

    def decrypt(self, cipher_text):
        plain_text_digrams_list = []
        for emoji in cipher_text:
            digram = self.map[emoji]
            plain_text_digrams_list.append(digram)
        return "".join(plain_text_digrams_list)

if __name__ == '__main__':
    dec = DigremojiCipher()

    # cipher_text = dec.encrypt("hello world digremoji")
    # print(cipher_text)
    # print(dec.decrypt(cipher_text))

    cipher_text = dec.encrypt("go north towards the river    take the dishwasher    fill it with tablets")
    print(cipher_text)
    print(dec.decrypt(cipher_text))



