import random

with open("digremoji_alphabet_with_spaces.txt", "r") as f:
    emojis = f.read()


shuffled_list = list(emojis)
random.shuffle(shuffled_list)

with open("digremoji_alphabet_with_spaces_shuffled.txt", "w") as f:
    f.write("".join(shuffled_list))