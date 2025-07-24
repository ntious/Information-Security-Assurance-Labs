import string

def generate_substitution_key():
    import random
    letters = list(string.ascii_uppercase)
    shuffled = letters.copy()
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def encrypt(text, key):
    return ''.join(key.get(c, c) for c in text.upper())

def decrypt(text, key):
    reverse_key = {v: k for k, v in key.items()}
    return ''.join(reverse_key.get(c, c) for c in text.upper())
