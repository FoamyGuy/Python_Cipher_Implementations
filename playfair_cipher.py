import string


# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


class PlayfairCipher:
    ALPHABET = string.ascii_uppercase.replace("J", "")

    def __init__(self, passphrase):
        self.passphrase = passphrase
        self.matrix_1d_list = []
        if len(passphrase) > 25:
            raise ValueError("Passphrase must be less than 25 characters")

        for letter in passphrase:
            if letter not in self.matrix_1d_list:
                self.matrix_1d_list.append(letter)

        for letter in PlayfairCipher.ALPHABET:
            if letter not in self.matrix_1d_list:
                self.matrix_1d_list.append(letter)

    @property
    def matrix(self):
        return list(divide_chunks(self.matrix_1d_list, 5))

    def letter_location(self, letter):
        letter_index = self.matrix_1d_list.index(letter)
        return (letter_index // 5, letter_index % 5)

    @property
    def pretty_matrix_str(self):
        return "\n".join([" ".join(_row) for _row in self.matrix])

    def prepare_message(self, message):
        message_valid = False
        message_list = list(message)

        while not message_valid:
            #print("message valid while loop")
            message_valid = True

            for digram_index, digram in enumerate(list(divide_chunks(message_list, 2))):
                #print(f"message valid inner for loop digram: {digram}")

                # length 1 means this is the last digram and message
                # has odd length
                if len(digram) == 1:
                    message_list.append("X" if message_list[-1] != "X" else "Z")
                    break

                if digram[0] == digram[1]:
                    message_valid = False
                    #print("Digram is matching, adding filler")
                    message_list.insert((digram_index * 2) + 1,
                                        "X" if digram[0] != "X" else "Z")

                    # skip the rest of the for loop, jump back out to the next
                    # while loop iteration
                    break

        return "".join(message_list)
    def encrypt(self, plain_text):
        cipher_text_list = []
        prepared = self.prepare_message(plain_text.upper())
        #print(f"prepared: {prepared}")
        digrams = list(divide_chunks(prepared, 2))

        print(digrams)
        for digram_index, pair in enumerate(digrams):
            letter_0_loc = self.letter_location(pair[0])
            letter_1_loc = self.letter_location(pair[1])

            #print(f"letter0: {letter_0_loc}")
            #print(f"letter1: {letter_1_loc}")

            if letter_0_loc[0] == letter_1_loc[0]:
                #print("SAME ROW")
                cipher_text_list.append(self.matrix[letter_0_loc[0]][(letter_0_loc[1] + 1) % 5])
                cipher_text_list.append(self.matrix[letter_1_loc[0]][(letter_1_loc[1] + 1) % 5])
            elif letter_0_loc[1] == letter_1_loc[1]:
                #print("SAME COL")
                cipher_text_list.append(self.matrix[(letter_0_loc[0] + 1) % 5][letter_0_loc[1]])
                cipher_text_list.append(self.matrix[(letter_1_loc[0] + 1) % 5][letter_1_loc[1]])
            else:
                #print("DIFF ROW & COL")
                cipher_text_list.append(self.matrix[letter_0_loc[0]][letter_1_loc[1]])
                cipher_text_list.append(self.matrix[letter_1_loc[0]][letter_0_loc[1]])
        return "".join(cipher_text_list)

    def decrypt(self, cipher_text, attempt_clean=False):
        clear_text_list = []
        prepared = self.prepare_message(cipher_text.upper())
        digrams = list(divide_chunks(prepared, 2))

        print(digrams)
        for digram_index, pair in enumerate(digrams):
            letter_0_loc = self.letter_location(pair[0])
            letter_1_loc = self.letter_location(pair[1])

            #print(f"letter0: {letter_0_loc}")
            #print(f"letter1: {letter_1_loc}")

            if letter_0_loc[0] == letter_1_loc[0]:
                #print("SAME ROW")
                clear_text_list.append(self.matrix[letter_0_loc[0]][(letter_0_loc[1] - 1)])
                clear_text_list.append(self.matrix[letter_1_loc[0]][(letter_1_loc[1] - 1)])
            elif letter_0_loc[1] == letter_1_loc[1]:
                #print("SAME COL")
                clear_text_list.append(self.matrix[(letter_0_loc[0] - 1)][letter_0_loc[1]])
                clear_text_list.append(self.matrix[(letter_1_loc[0] - 1)][letter_1_loc[1]])
            else:
                #print("DIFF ROW & COL")
                clear_text_list.append(self.matrix[letter_0_loc[0]][letter_1_loc[1]])
                clear_text_list.append(self.matrix[letter_1_loc[0]][letter_0_loc[1]])

        if attempt_clean:
            #print("attempting to clean")
            unchanged = False
            while not unchanged:
                unchanged = True
                for index, letter in enumerate(clear_text_list):
                    # if it's a filler letter
                    if letter in ("X", "Z"):
                        # if surrounding letters are same
                        try:
                            if clear_text_list[index-1] == clear_text_list[index+1]:
                                #print(f"removing index {index}")
                                clear_text_list.pop(index)
                                unchanged = False
                                break
                        except IndexError:
                            pass
            if clear_text_list[-1] in ("X", "Z"):
                clear_text_list.pop(len(clear_text_list) - 1)

        return "".join(clear_text_list)

if __name__ == '__main__':
    pfc = PlayfairCipher(passphrase="WHEATSTONE")
    print(pfc.matrix)

    print(pfc.pretty_matrix_str)

    #print(pfc.prepare_message("HELLOP"))

    cipher_text = pfc.encrypt("RAZZLE")
    print(cipher_text)
    clear_text = pfc.decrypt(cipher_text, attempt_clean=True)
    print(clear_text)


    # cipher_text = pfc.encrypt("roooom")
    # print(cipher_text)
    # clear_text = pfc.decrypt(cipher_text, attempt_clean=True)
    # print(clear_text)

