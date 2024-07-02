from random import choices
from string import ascii_lowercase, digits

t = ascii_lowercase + digits * 6

def ran_char_num():
    return ''.join(choices(t,k=5))

