# Lab: OpenSSL Essentials – AES, RSA, and Hashes

## 🎯 Objective

The purpose of this lab is to help students **gain hands-on experience with modern cryptography** using the OpenSSL toolkit.  
You will practice **symmetric encryption (AES), asymmetric encryption (RSA keypairs), hashing (SHA-256), and digital signatures**, learning how these techniques protect confidentiality, integrity, and authenticity.

---

## 📖 Background

Unlike classical ciphers, modern cryptography uses **mathematical algorithms** that are still secure today when properly applied:

- **AES (Advanced Encryption Standard)**: Fast symmetric algorithm for encrypting bulk data.  
- **RSA**: Asymmetric algorithm for key exchange and digital signatures.  
- **SHA-256**: Secure hash function to ensure data integrity.  
- **Digital Signatures**: Combine hashing + RSA to verify authenticity.

This activity supports the course learning outcome:  
👉 **Demonstrate basic encryption and decryption using industry-standard tools (OpenSSL).**

---

## 🛠️ Prerequisites

* GitHub Codespaces or local Linux/WSL environment with:
  - **OpenSSL 3.0+**
  - **Python 3.11+** (installed via `.devcontainer`)
* Basic understanding of symmetric vs asymmetric encryption

---

## 📝 Tasks

### Step 1 – AES File Encryption & Decryption
1. Navigate to the lab folder:
   ```bash
   cd labs/Encryption/lab_encryption_modern/01_openssl
````

2. Encrypt the provided file:

   ```bash
   bash scripts/aes_encrypt.sh sample.txt secret.enc
   ```
3. Decrypt the file:

   ```bash
   bash scripts/aes_decrypt.sh secret.enc recovered.txt
   ```
4. Verify that `sample.txt` and `recovered.txt` are identical:

   ```bash
   diff sample.txt recovered.txt
   ```

---

### Step 2 – RSA Keypair Generation

1. Generate a public/private keypair:

   ```bash
   bash scripts/rsa_keypair.sh
   ```
2. This creates:

   * `private.pem` (keep secret, use for signing/decryption)
   * `public.pem` (share with others, use for verification/encryption)

---

### Step 3 – Digital Signatures

1. Sign a file with your **private key**:

   ```bash
   bash scripts/sign.sh sample.txt signature.bin private.pem
   ```
2. Verify the signature with the **public key**:

   ```bash
   bash scripts/verify.sh sample.txt signature.bin public.pem
   ```
3. Try altering `sample.txt` and re-running verification — it should fail.

---

### Step 4 – Hashing

1. Generate a SHA-256 hash:

   ```bash
   openssl dgst -sha256 sample.txt
   ```
2. Discuss: how does hashing differ from encryption?

---

### (Optional Bonus) Hybrid Encryption

1. Generate a random AES key:

   ```bash
   openssl rand -base64 32 > aes.key
   ```
2. Encrypt the AES key with your **public RSA key**:

   ```bash
   openssl rsautl -encrypt -inkey public.pem -pubin -in aes.key -out aes.key.enc
   ```
3. Decrypt the AES key with your **private RSA key**:

   ```bash
   openssl rsautl -decrypt -inkey private.pem -in aes.key.enc -out aes.key.dec
   ```
4. Compare `aes.key` and `aes.key.dec` — they should match.

---

## 📂 Deliverables

* A short **report** (Markdown, Word, or PDF) including:

  * Screenshots of AES encryption/decryption working
  * Evidence of successful RSA keypair generation
  * Signature + verification output
  * SHA-256 hash of `sample.txt`
  * (Optional) Evidence of hybrid encryption working
* Reflection: Explain when you would use AES vs RSA in real-world systems.

---

## ✅ Evaluation Criteria

* **Completion** – All AES, RSA, signature, and hash tasks attempted
* **Accuracy** – Commands run correctly; decrypted files match originals
* **Analysis** – Clear explanation of symmetric vs asymmetric, and the role of hashing
* **Presentation** – Screenshots + reflections presented neatly

---

## 📘 Learning Outcomes

By completing this lab, you will be able to:

* Encrypt and decrypt files with AES using OpenSSL
* Generate RSA public/private keypairs and understand their purpose
* Create and verify digital signatures
* Use hashing for data integrity checks
* Explain the difference between symmetric and asymmetric cryptography

---

## ⚠️ Ethical Reminder

Keys and certificates generated in this lab are for **educational purposes only**.
Do not use these test keys in any real system.
Always protect private keys and delete them (`make clean`) when finished.
----