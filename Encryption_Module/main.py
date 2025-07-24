import sys
from encryption import caesar, aes, rsa
from utils.file_io import read_text, write_text

def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <technique> <input_file> <encrypt/decrypt>")
        return

    technique = sys.argv[1]
    filepath = sys.argv[2]
    mode = sys.argv[3].lower()

    plaintext = read_text(filepath)

    if technique == 'caesar':
        shift = 3
        if mode == 'encrypt':
            ciphertext = caesar.encrypt(plaintext, shift)
            write_text('outputs/caesar_encrypted.txt', ciphertext)
        elif mode == 'decrypt':
            decrypted = caesar.decrypt(plaintext, shift)
            write_text('outputs/caesar_decrypted.txt', decrypted)

    elif technique == 'aes':
        if mode == 'encrypt':
            aes.encrypt_to_file(plaintext, 'outputs/aes_encrypted.txt')
        elif mode == 'decrypt':
            aes.decrypt_from_file('outputs/aes_encrypted.txt', 'outputs/aes_decrypted.txt')

    elif technique == 'rsa':
        if mode == 'encrypt':
            rsa.encrypt_to_file(plaintext, 'outputs/rsa_encrypted.txt')
        elif mode == 'decrypt':
            rsa.decrypt_from_file('outputs/rsa_encrypted.txt', 'outputs/rsa_decrypted.txt')

    else:
        print("Unsupported technique.")

if __name__ == '__main__':
    main()
