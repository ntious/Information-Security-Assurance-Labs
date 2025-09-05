# Lab 01 — OpenSSL Essentials (AES/RSA/Hashes)

**Objectives**
- Encrypt/decrypt a file with AES-256-CBC.
- Generate an RSA keypair; sign and verify a message.
- Compute and compare SHA-256 hashes.

**Start**
```bash
cd labs/Encryption/lab_encryption_modern/01_openssl
bash scripts/aes_encrypt.sh sample.txt secret.enc
bash scripts/aes_decrypt.sh secret.enc recovered.txt

bash scripts/rsa_keypair.sh     # private.pem, public.pem
bash scripts/sign.sh sample.txt signature.bin private.pem
bash scripts/verify.sh sample.txt signature.bin public.pem

openssl dgst -sha256 sample.txt
```

**Deliverables**
1. Screenshot or paste of successful decryption diff (`diff sample.txt recovered.txt` has no output).
2. `openssl dgst -sha256 sample.txt` output.
3. One paragraph: symmetric vs asymmetric—when to use each.
