# Simulate a digital signature using RSA and hashlib (not secure for real use)
import rsa
import hashlib

(pub, priv) = rsa.newkeys(512)

def sign_message(message):
    hashed = hashlib.sha256(message.encode()).digest()
    signature = rsa.sign(hashed, priv, 'SHA-256')
    return signature

def verify_signature(message, signature):
    hashed = hashlib.sha256(message.encode()).digest()
    try:
        rsa.verify(hashed, signature, pub)
        return True
    except rsa.VerificationError:
        return False

if __name__ == "__main__":
    msg = "This is a digitally signed message."
    sig = sign_message(msg)
    print("Signature valid:", verify_signature(msg, sig))
