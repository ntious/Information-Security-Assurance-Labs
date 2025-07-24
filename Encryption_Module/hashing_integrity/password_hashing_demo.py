import hashlib
import os

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    pwd_salt = password.encode() + salt
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex(), hashed.hex()

def verify_password(input_password, stored_salt, stored_hash):
    salt = bytes.fromhex(stored_salt)
    _, input_hash = hash_password(input_password, salt)
    return input_hash == stored_hash

if __name__ == "__main__":
    # Demo use
    password = input("Enter password to hash: ")
    salt, hash_val = hash_password(password)
    print(f"Salt: {salt}")
    print(f"Hash: {hash_val}")

    test_pw = input("Re-enter password to verify: ")
    if verify_password(test_pw, salt, hash_val):
        print("Password verified ✅")
    else:
        print("Password mismatch ❌")
