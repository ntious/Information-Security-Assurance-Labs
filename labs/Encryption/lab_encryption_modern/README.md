# 🔐 Modern Encryption & Protocol Labs

This module contains **hands-on labs using industry-standard tools**.  
It extends the classical ciphers labs by focusing on **modern cryptography and secure communication protocols**.

> 🎯 **Learning Outcome**  
> *Demonstrate basic encryption and decryption using industry-standard tools (e.g., OpenSSL) and explain the role of protocols such as SSL/TLS, VPNs, and SSH in securing communications.*

---

## 📚 Labs in This Module

1. **Lab 01 — OpenSSL Essentials**  
   - Encrypt/decrypt files with AES-256.  
   - Generate RSA keypairs.  
   - Create and verify digital signatures.  
   - Compute SHA-256 hashes.

2. **Lab 02 — TLS/SSL in Practice**  
   - Inspect certificates of real-world websites.  
   - Identify TLS versions, cipher suites, and certificate chains.  
   - Run a local TLS echo server with a self-signed certificate.  

3. **Lab 03 — SSH Keys & Secure Remote**  
   - Generate SSH keypairs.  
   - Verify host fingerprints and avoid MITM attacks.  
   - Connect securely to GitHub using SSH authentication.  

4. **Lab 04 — VPN Concepts (Config Anatomy)**  
   - Analyze WireGuard and OpenVPN configuration files.  
   - Understand how VPNs establish encrypted tunnels.  
   - Compare VPNs with TLS and SSH.  

---

## ⚙️ Getting Started (Codespaces Recommended)

1. Open this repo in **GitHub Codespaces**.  
2. Verify the environment:  
```bash
   make check
````

3. Navigate to the desired lab folder and follow its `README.md`.
   Example for Lab 01:

   ```bash
   cd labs/Encryption/lab_encryption_modern/01_openssl
   ```

---

## 🛠 Using the Makefile

At the repository root, a **Makefile** provides shortcuts for testing and cleaning labs:

```bash
make check      # Verify environment (OpenSSL + Python)
make openssl    # Run Lab 01 OpenSSL test
make tls        # Run Lab 02 TLS certificate test
make tls-run    # Start the TLS echo server (Lab 02)
make ssh        # Run Lab 03 SSH test
make vpn        # Confirm Lab 04 VPN configs exist
make clean      # Remove generated keys/certs (safety)
make all        # Run all checks in sequence
```

💡 **Tip:** Always run `make clean` before committing to GitHub to avoid pushing private keys or certs.

---

## 📂 Structure

```
lab_encryption_modern/
├── 01_openssl/         → AES, RSA, signatures, hashes
├── 02_tls/             → TLS inspection + local echo server
├── 03_ssh/             → SSH keys & GitHub demo
└── 04_vpn/             → WireGuard & OpenVPN config analysis
```

---

## 📝 Deliverables

Each lab requires:

* **Execution evidence** (screenshots, command output).
* **Short reflection** (1–2 paragraphs explaining what you did and why it matters).

Submit your work through the platform/instructions provided by your instructor.

---

## 🛡️ Notes

* Use only **self-signed certificates** or provided configs — never real private keys.
* Do not connect to unauthorized systems.
* Labs are for **educational purposes only**.

---

🎓 *These modern labs ensure you gain practical experience with the tools and protocols that secure today’s digital communications.*

```
