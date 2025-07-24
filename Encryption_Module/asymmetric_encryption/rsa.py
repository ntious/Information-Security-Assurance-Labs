import rsa

(pubkey, privkey) = rsa.newkeys(512)

def encrypt_to_file(plaintext, out_path):
    encrypted = rsa.encrypt(plaintext.encode(), pubkey)
    with open(out_path, 'wb') as f:
        f.write(encrypted)
    return encrypted

def decrypt_from_file(enc_path, out_path):
    with open(enc_path, 'rb') as f:
        encrypted = f.read()
    decrypted = rsa.decrypt(encrypted, privkey).decode()
    with open(out_path, 'w') as f:
        f.write(decrypted)
