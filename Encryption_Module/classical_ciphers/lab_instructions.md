# Classical Cipher Lab Instructions

This folder contains Python implementations of three classical encryption techniques:

- **Caesar Cipher** – Simple letter shift
- **Substitution Cipher** – Random letter mapping
- **Vigenère Cipher** – Polyalphabetic cipher based on a key

## ✅ Instructions

1. Open each script and explore the `encrypt` and `decrypt` functions.
2. Modify `main.py` or create your own driver to:
   - Read `plaintext.txt`
   - Encrypt it using a chosen cipher
   - Save the result to `outputs/`
   - Decrypt the ciphertext and verify it matches the original

## ✏️ Example Caesar Cipher Usage

```python
from caesar_cipher import caesar_encrypt, caesar_decrypt

plaintext = "HELLO WORLD"
cipher = caesar_encrypt(plaintext, 3)
plain = caesar_decrypt(cipher, 3)
```

Try with different messages and shifts. Use print statements or output to `.txt` files.
