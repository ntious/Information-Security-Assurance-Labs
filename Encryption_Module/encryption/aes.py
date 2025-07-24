from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_to_file(plaintext, out_path):
    ciphertext = cipher.encrypt(plaintext.encode())
    with open(out_path, 'wb') as f:
        f.write(ciphertext)
    return ciphertext

def decrypt_from_file(enc_path, out_path):
    with open(enc_path, 'rb') as f:
        ciphertext = f.read()
    decrypted = cipher.decrypt(ciphertext).decode()
    with open(out_path, 'w') as f:
        f.write(decrypted)
