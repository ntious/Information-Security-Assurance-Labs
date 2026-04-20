# 🧩 Classical Ciphers Toolkit

This Python toolkit is an **interactive playground for classical cryptography**.
It allows students to explore, encrypt, decrypt, and experiment with **11 major historical ciphers** in a hands-on, menu-driven environment.

⚠️ **Note**: This lab is for **educational use only**. These ciphers are not secure by modern standards and should not be used in real-world applications.

---

## 🚀 Run in Your Browser (No Installation Needed)

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ntious/Information-Security-Assurance-Labs/HEAD?urlpath=lab/tree/labs/Encryption/lab_encryption_classical)

Binder allows you to run this lab directly in your browser without installing Python.

### ▶️ How to Run in Binder

Once Binder loads:

1. Open **Terminal** from JupyterLab (top menu → *File → New → Terminal*)
2. Run the script:

```bash
python classical_ciphers_toolkit.py
```

3. Use the interactive cipher menu in the terminal

> 💡 This lab is designed as a **Python script**, not a notebook.
> Students interact with it via the terminal.

---

## ✨ Features

The toolkit includes:

1. **Caesar Cipher** – Shift-based substitution
2. **Atbash Cipher** – Alphabet reversal
3. **Affine Cipher** – Linear transformation using keys `a` and `b`
4. **Vigenère Cipher** – Keyword-based polyalphabetic cipher
5. **Rail Fence Cipher** – Zigzag transposition
6. **Columnar Transposition Cipher** – Keyword-based column rearrangement
7. **Playfair Cipher** – 5×5 digraph substitution
8. **Hill Cipher (2×2)** – Matrix-based encryption (requires `numpy`)
9. **Autokey Cipher** – Key extended with plaintext
10. **Beaufort Cipher** – Variant of Vigenère (symmetric)
11. **Hybrid Cipher (Caesar → Atbash)** – Layered transformation

---

## 🚀 Getting Started (Local Setup)

### Requirements

* Python **3.7+**
* `numpy` (for Hill Cipher)

Install dependencies:

```bash
pip install numpy
```

---

### ▶️ Run Locally

```bash
python classical_ciphers_toolkit.py
```

---

### 🧭 Example Menu

```text
=== Classical Ciphers Toolkit ===
1 - Caesar | 2 - Atbash | 3 - Affine | 4 - Vigenere
5 - Rail Fence | 6 - Columnar | 7 - Playfair | 8 - Hill
9 - Autokey | 10 - Beaufort | 11 - Hybrid (Caesar→Atbash) | Q - Quit
Choose:
```

---

## 🕹️ Usage Guide

Typical workflow:

* **Encrypt** → input plaintext + key(s) → get ciphertext
* **Decrypt** → input ciphertext + key(s) → recover plaintext

Notes:

* Some ciphers remove spaces
* Some pad text with `X` (e.g., Hill, Playfair)
* Keys must follow cipher-specific rules

---

## 📚 Learning Concepts

### 🔐 Substitution Ciphers

* Caesar, Affine, Vigenère, Atbash, Beaufort, Autokey

### 🔄 Transposition Ciphers

* Rail Fence, Columnar

### 🔢 Polygraphic Ciphers

* Playfair, Hill

### 🧪 Hybrid Systems

* Demonstrates layered encryption approaches

💡 This toolkit shows how cryptography evolved from simple substitution to structured, multi-step systems.

---

## ✅ Quick Sanity Tests

Students can quickly verify correctness:

* Caesar: `"HELLO"`, step=3 → `KHOOR` → back: `HELLO`
* Atbash: `"HELLO WORLD"` → `SVOOL DLIOW` → back: `HELLO WORLD`
* Affine: `a=5, b=8, "HELLO"` → `RCLLA` → back: `HELLO`
* Vigenère: key=`KEY`, `"HELLO"` → `RIJVS` → back: `HELLO`
* Rail Fence: rails=3, `"HELLO WORLD"` → `HOOLELWRDL` → back: `HELLO WORLD`
* Columnar: key=`ZEBRA`, `"HELLO WORLD"` → `LWDLOOERHLX` → back: `HELLOWORLD`
* Playfair: key=`MONARCHY`, `"HELLO WORLD"` → `KBMODZBXDM` → back: `HELXLOWORLDX`
* Hill: key=`[[3,3],[2,5]]`, `"HELLO"` → `MFNCX` → back: `HELLOX`
* Autokey: key=`KEY`, `"HELLOWORLD"` → verify encrypt/decrypt
* Beaufort: key=`KEY`, `"HELLO"` → `DRJIY` → back: `HELLO`
* Hybrid: step=3, `"HELLO"` → `PSLLI` → back: `HELLO`

---

## 🛠️ Extending the Toolkit

Students can extend the project by:

* Adding new ciphers (ROT13, Bacon’s cipher, Enigma simulation)
* Implementing **frequency analysis attacks**
* Adding CLI support using `argparse`
* Comparing cipher strengths and weaknesses
* Building visualization tools for cipher transformations

---

## 📖 Educational Purpose

This lab supports the learning outcome:

👉 **Understand fundamental cryptographic techniques through hands-on experimentation**

It highlights:

* The **limitations of classical encryption**
* The importance of **key management**
* Why modern cryptography is necessary

---

## ⚙️ Binder Configuration (Important for Instructors)

To ensure Binder works correctly, your repository must include:

```text
Information-Security-Assurance-Labs/
├── .binder/
│   ├── requirements.txt
│   └── runtime.txt
├── Encryption/
│   └── lab_encryption_classical/
│       ├── classical_ciphers_toolkit.py
│       ├── README.md
│       ├── LAB_INSTRUCTIONS.md
│       ├── INSTRUCTOR_NOTES.md
│       └── STUDENT_USAGE.md
```

### `.binder/requirements.txt`

```txt
numpy
notebook
jupyterlab
ipykernel
```

### `.binder/runtime.txt`

```txt
python-3.11
```

> ⚠️ Binder will **fail** if environment files are not in the repo root or `.binder/`.

---

## 🎓 Author

**I. K. Nti**
Assistant Professor – Information Technology
For educational use only

---

## 📌 Final Note

This toolkit is intentionally **simple, transparent, and interactive**
to help students *see* how encryption works — not just use it.

---
