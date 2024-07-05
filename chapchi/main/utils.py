import os
from random import choices
from string import ascii_lowercase, digits

t = ascii_lowercase + digits * 6 # balance between lowercase and digits; ascii:28, digits:10


def ran_char_num():
    return ''.join(choices(t,k=5))

def generate_file_tree(directory):
    file_tree = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('X') and len(file) > 5:
                code = file[1:6]  # Extract the 5-digit code
                file_tree[code] = file
    return file_tree