import random
import string

def generate_group_code(length=10):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))