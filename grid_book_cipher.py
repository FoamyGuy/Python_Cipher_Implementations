import string
import secrets

from book_cipher import BookCipher


class GridBookCipher(BookCipher):
    def __init__(self, book_grid_str=None, grid_width=10, grid_height=10):
        self.force_uppercase = True
        self.swaps = {" ": "_", "_": " "}
        if book_grid_str is None:
            self.book_grid = GridBookCipher.init_book(grid_width, grid_height)
        else:
            self.book_grid = GridBookCipher.parse_book_grid_str(book_grid_str)
    @property
    def book_str(self):
        return "".join(["".join(_row) for _row in self.book_grid])

    @staticmethod
    def init_book(grid_width, grid_height):
        book_length = grid_width * grid_height
        alphabet = string.ascii_uppercase + "_"
        full_sets = book_length // len(alphabet)
        leftover = book_length - (full_sets * len(alphabet))

        #print(f"full_sets: {full_sets} | leftover: {leftover}")
        pool = list(alphabet * full_sets)

        full_grid = []
        for i in range(grid_height):
            row = []
            for i in range(grid_width):
                if len(pool):
                    if leftover and secrets.randbelow(full_sets + 2) == 0:
                        #print(f"lucky roll. still have {leftover} leftovers.")
                        letter = secrets.choice("RSTALNEI_")
                        leftover -= 1
                    else:
                        chosen_index = secrets.randbelow(len(pool))
                        letter = pool.pop(chosen_index)

                else:
                    letter = secrets.choice("RSTALNEI_")
                    leftover -= 1
                row.append(letter)
            full_grid.append(row)

        return full_grid

    @staticmethod
    def parse_book_grid_str(book_str):
        book_grid = []
        for input_row in book_str.split("\n"):
            book_grid.append(input_row.split(" "))
        return book_grid

    def pretty_grid_str(self):
        return "\n".join([" ".join(_row) for _row in self.book_grid])


if __name__ == '__main__':
    # gbc = GridBookCipher()
    # print(gbc.pretty_grid_str())
    # print()
    # print(gbc.book_str)

    # for letter in string.ascii_uppercase + "_":
    #     print(f"{letter}: {gbc.book_str.count(letter)}")

    # cipher_test_list = gbc.encrypt("YYY YYY YYY")
    # print(cipher_test_list)
    # print(gbc.decrypt(cipher_test_list))

    gbc = GridBookCipher()
    print(gbc.pretty_grid_str())
    print()
    cipher_test_list = gbc.encrypt("how about lowercase?")
    print(cipher_test_list)
    print(gbc.decrypt(cipher_test_list))
