# 🧩 Classical Ciphers Toolkit

This Python toolkit is an **interactive playground for classical cryptography**.
It allows students to explore, encrypt, decrypt, and experiment with **11 major historical ciphers**.

⚠️ **Note**: This lab is for **educational use only**. These ciphers are not secure by modern standards and should not be used in real-world applications.

# 🧩 Classical Ciphers Toolkit

[![Launch Binder](https://mybinder.org/badge_logo.svg)](
https://mybinder.org/v2/gh/ntious/Information-Security-Assurance-Labs/HEAD?filepath=labs/Encryption/lab_encryption_classical/classical_ciphers_toolkit.ipynb
)

This Python toolkit is an **interactive playground for classical cryptography**.

---

## ✨ Features

The toolkit includes:

1. **Caesar Cipher** (shift-based)
2. **Atbash Cipher** (reversal substitution)
3. **Affine Cipher** (linear substitution, `a` and `b` keys)
4. **Vigenère Cipher** (keyword-based shift)
5. **Rail Fence Cipher** (zigzag transposition)
6. **Columnar Transposition Cipher** (keyword columnar readout)
7. **Playfair Cipher** (5×5 digraph substitution)
8. **Hill Cipher (2×2)** (matrix-based substitution)
9. **Autokey Cipher** (key extended with plaintext)
10. **Beaufort Cipher** (variant of Vigenère, symmetric)
11. **Hybrid Caesar → Atbash** (Caesar shift, then Atbash)

---

## 🚀 Getting Started

### Requirements

* Python **3.7+**
* `numpy` library (for Hill cipher math):

  ```bash
  pip install numpy
  ```

### Running the Toolkit

Run the main script:

```bash
python classical_ciphers_toolkit.py
```

You’ll see a menu like:

```
=== Classical Ciphers Toolkit ===
1 - Caesar | 2 - Atbash | 3 - Affine | 4 - Vigenere
5 - Rail Fence | 6 - Columnar | 7 - Playfair | 8 - Hill
9 - Autokey | 10 - Beaufort | 11 - Hybrid (Caesar→Atbash) | Q - Quit
Choose:
```

---

## 🕹️ Usage Guide

Each cipher has its own menu. Typical flow:

* **Encrypt** → type text + key(s) → ciphertext generated.
* **Decrypt** → type ciphertext + key(s) → plaintext recovered.
* Some ciphers strip spaces or pad with `X` (e.g., Hill, Playfair).

---

## 📚 Learning Notes

* **Substitution Ciphers** → Caesar, Affine, Vigenère, Atbash, Beaufort, Autokey
* **Transposition Ciphers** → Rail Fence, Columnar
* **Polygraphic Ciphers** → Playfair, Hill (block-based)
* **Hybrids** → show layered security approaches

💡 This toolkit illustrates the **evolution of cryptography** from simple shifts to more complex block and polygraphic systems.

---

## ✅ Quick Sanity Tests

Students can immediately test:

* Caesar: `"HELLO"`, step=3 → `KHOOR` → back: `HELLO`
* Atbash: `"HELLO WORLD"` → `SVOOL DLIOW` → back: `HELLO WORLD`
* Affine: `a=5, b=8, "HELLO"` → `RCLLA` → back: `HELLO`
* Vigenère: key=`KEY`, `"HELLO"` → `RIJVS` → back: `HELLO`
* Rail Fence: rails=3, `"HELLO WORLD"` → `HOOLELWRDL` → back: `HELLO WORLD`
* Columnar: key=`ZEBRA`, `"HELLO WORLD"` → `LWDLOOERHLX` → back: `HELLOWORLD`
* Playfair: key=`MONARCHY`, `"HELLO WORLD"` → `KBMODZBXDM` → back: `HELXLOWORLDX`
* Hill: key=`[[3,3],[2,5]]`, `"HELLO"` → `MFNCX` → back: `HELLOX`
* Autokey: key=`KEY`, `"HELLOWORLD"` → encrypted/decrypted test
* Beaufort: key=`KEY`, `"HELLO"` → `DRJIY` → back: `HELLO`
* Hybrid: step=3, `"HELLO"` → `PSLLI` → back: `HELLO`

---

## 🛠️ Extending the Toolkit

Ideas for students:

* Add new ciphers (e.g., ROT13, Bacon’s, Enigma simulation).
* Add CLI options (`argparse`) for automation.
* Try building **cipher-breaking tools** with frequency analysis.

---

## 📖 Educational Purpose

This lab connects to the course outcome:
👉 **Understand fundamental cryptographic techniques by experimenting with classical ciphers.**

It demonstrates the **limitations of early encryption methods**, paving the way for modern cryptography.

---

🎓 **Enjoy exploring classical cryptography!**

By: *I. K. Nti* (for educational purposes only)


---
