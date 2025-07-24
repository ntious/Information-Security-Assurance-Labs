def encrypt(text, shift):
    return ''.join(chr((ord(c) - 65 + shift) % 26 + 65) if c.isupper() else c for c in text)

def decrypt(text, shift):
    return encrypt(text, -shift)
