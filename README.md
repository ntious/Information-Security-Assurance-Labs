
# Information Security and Assurance – Educational Labs

Welcome to the **Information Security and Assurance (ISA)** course repository.
This repository provides **hands-on labs** and resources that align with the course learning outcomes.

> ⚠️ **Disclaimer**
> All content in this repository is for **educational purposes only**. Do not use these materials for malicious purposes. Misuse is strictly prohibited.

---

## 📚 Course Learning Outcomes

Upon completion of this course, students will be able to:

1. **Identify and prioritize information assets**
2. **Identify and prioritize threats to information assets**
3. **Define an information security strategy and architecture**
4. **Plan for and respond to intruders in an information system**
5. **Identify types of ethical issues regarding IT in daily life**
6. **Understand and apply security/privacy-related laws, regulations, and standards**
7. **Present a disaster recovery plan for recovery of information assets after an incident**
8. **Demonstrate basic encryption and decryption using industry-standard tools (e.g., OpenSSL) and explain the role of protocols such as SSL/TLS, VPNs, and SSH in securing communications**

---

## 🧪 Labs Aligned to Outcomes

Each lab supports one or more outcomes.

### Asset Identification & Risk Assessment Labs

* **Lab 1: Asset Inventory**
  *Outcome 1* – Create an inventory of IT assets (hardware, software, data) and classify their value.
* **Lab 2: Asset Prioritization**
  *Outcome 1, 2* – Prioritize assets based on risk and business impact.
* **Lab 3: Threat & Vulnerability Identification**
  *Outcome 2* – Identify common threats/vulnerabilities against assets.
* **Lab 4: Qualitative Risk Assessment**
  *Outcome 2, 3* – Build a risk matrix to assess likelihood and impact.
* **Lab 5: Risk Mitigation Strategies**
  *Outcome 3* – Propose layered controls and mitigations.

### Encryption Labs

* **Classical Ciphers Toolkit**
  *Foundation* – Explore 11 classical ciphers (Caesar, Vigenère, Playfair, Rail Fence, etc.).
  Builds intuition on substitution/transposition and prepares students for modern cryptography.

* **Modern Encryption & Protocols**
  *Outcome 8* – Meet the industry-standard tools requirement.

  * **Lab 01: OpenSSL Essentials** — AES, RSA, digital signatures, and hashing.
  * **Lab 02: TLS/SSL in Practice** — Inspect certificates and run a local TLS echo server.
  * **Lab 03: SSH Keys & Secure Remote** — Generate keys, verify host fingerprints, and connect to GitHub via SSH.
  * **Lab 04: VPN Concepts** — Explore WireGuard/OpenVPN configs and explain how VPNs secure communications.

---

## ⚙️ Setup Instructions

You can run labs in **GitHub Codespaces** (recommended) or locally.

### Option 1: Run in Codespaces

1. Fork this repository.
2. Launch in **GitHub Codespaces**.
3. Run the environment check:

   ```bash
   make check
   ```
4. Navigate to the lab folder you want and follow its `README.md`.

### Option 2: Run Locally

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
```

---

## 📂 Repository Structure

```
labs/
├── Asset Identification and Risk Assessment/
│   ├── lab1_asset_inventory/
│   ├── lab2_asset_prioritization/
│   ├── lab3_threat_vulnerability_identification/
│   ├── lab4_risk_assessment_qualitative/
│   └── lab5_risk_mitigation_strategies/
│
└── Encryption/
    ├── lab_encryption_classical/
    │   ├── classical_ciphers_toolkit.py
    │   └── LAB_INSTRUCTIONS.md
    │
    └── lab_encryption_modern/
        ├── 01_openssl/
        ├── 02_tls/
        ├── 03_ssh/
        └── 04_vpn/

.devcontainer/   → Codespaces setup  
Makefile         → Quick lab checks  
README.md        → Course overview
```

---

## 🛡️ Learning Philosophy

These labs are designed to **bridge theory with practice**, giving students not just academic knowledge but also the ability to simulate real-world security scenarios.
Students will learn both **foundational principles** (classical ciphers, asset identification) and **modern practices** (OpenSSL, TLS, SSH, VPN).

---

## 📜 License

This repository is licensed under the **MIT License** for educational use only.

---

🎓 *By: I. K. Nti* (for educational purposes only)

---
