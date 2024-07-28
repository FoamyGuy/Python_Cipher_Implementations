import string
import random


class JeffersonDiskCipher:
    def __init__(self, disks_str=None):
        self.disks = []

        if disks_str is None:
            for i in range(36):
                new_disk = list(string.ascii_uppercase)
                random.shuffle(new_disk)
                self.disks.append("".join(new_disk))
        else:
            self.disks = JeffersonDiskCipher.parse_disks(disks_str)
        self.disk_rotation_indexes = [0] * len(self.disks)

    def visible_row(self, index):
        display_str_list = []
        for i in range(len(self.disks)):
            display_str_list.append(
                self.disks[i][(index + self.disk_rotation_indexes[i]) % len(self.disks[i])]
            )
        return "".join(display_str_list)

    def reset_disk_rotations(self):
        for i in range(len(self.disk_rotation_indexes)):
            self.disk_rotation_indexes[i] = 0
    @staticmethod
    def parse_disks(disks_str):
        disks = []
        for row in disks_str.split("\n"):
            this_row_disks = row.split("  ")
            disks.extend(this_row_disks)
        return disks

    def pretty_disks(self):
        rows = []
        for i in range(36 // 3):
            rows.append(f"{self.disks[i * 3]}  {self.disks[i * 3 + 1]}  {self.disks[i * 3 + 2]}")
        return "\n".join(rows)

    def encrypt(self, clear_text, rotation_index=1):
        clear_text = clear_text.upper()
        if rotation_index == 0:
            raise ValueError("Rotation index of 0 would result in clear text")
        if len(clear_text) > len(self.disks):
            raise ValueError("Clear text length must not exceed the number of disks")

        if len(clear_text) < len(self.disks):
            clear_text += "A" * (len(self.disks) - len(clear_text))

        for index, letter in enumerate(clear_text):
            self.disk_rotation_indexes[index] = self.disks[index].index(letter)

        return self.visible_row(rotation_index)

    def decrypt(self, cipher_text, rotation_index=1):
        if len(cipher_text) != len(self.disks):
            raise ValueError("Cipher text length must equal the number of disks")

        for index, letter in enumerate(cipher_text):
            self.disk_rotation_indexes[index] = self.disks[index].index(letter)

        return self.visible_row(-rotation_index)

    def all_visible_rows(self):
        rows = []
        for i in range(len(self.disks[0])):
            rows.append(self.visible_row(i))
        return rows

if __name__ == '__main__':

    # jefferson = JeffersonDiskCipher()
    # print(jefferson.pretty_disks())
    # print()
    # # print(jefferson.disks)
    # # print(jefferson.visible_row(0))
    #
    # cipher_text = jefferson.encrypt("ChocolateEsspressoCupcake")
    # print(cipher_text)
    # jefferson.reset_disk_rotations()
    #
    # clear_text = jefferson.decrypt(cipher_text)
    # print(clear_text)
    # print()
    # print("All visible rows:")
    # print("\n".join(jefferson.all_visible_rows()))


    jeff = JeffersonDiskCipher()
    print(jeff.pretty_disks())
    print()
    cipher_text = jeff.encrypt("BlueBagelsBoilingBananas", rotation_index=13)
    print(cipher_text)

    print(jeff.encrypt(cipher_text, rotation_index=13))

    pass
