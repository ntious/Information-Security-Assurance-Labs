# 🔐 **Lab: Exploring Classical Encryption**

## 🎯 **Lab Purpose**

In this lab, you will explore how early cryptographic systems worked by experimenting with a Python-based **Classical Ciphers Toolkit**. You will encrypt and decrypt messages using a variety of substitution and transposition ciphers, analyze how they operate, and understand **why classical ciphers became insecure over time**.

This lab supports the course outcome:
👉 **Apply cryptographic techniques to secure information and recognize their limitations.**

---

# 🧠 **Why This Matters**

Before modern encryption existed, early ciphers like **Caesar, Vigenère, Playfair, and Hill** were considered secure. Today, they can be broken quickly—even by beginners—because computing power and mathematical analysis have advanced.

Working with these ciphers helps you:

* Understand the *foundational ideas* behind encryption
* See how keys, shifts, and matrices transform plaintext
* Practice brute-force reasoning
* Appreciate the importance of modern cryptography like AES and RSA

---

# 🛠️ **What You Need Before Starting**

### ✅ Python 3.7 or above

### ✅ The `numpy` package (used for Hill cipher matrix operations)

Install if needed:

```bash
pip install numpy
```

### ✅ The provided file:

* `classical_ciphers_toolkit.py`

---

# 📂 **Lab Steps**

## **Step 1 — Launch the Toolkit**

From the terminal:

```bash
python classical_ciphers_toolkit.py
```

Browse the menu to see all available ciphers.
The toolkit lets you try **11 classical ciphers**, including:

* Caesar
* Vigenère
* Affine
* Atbash
* Playfair
* Rail Fence
* Hill
* …and more

---

## **Step 2 — Encrypt & Decrypt Sample Messages**

Choose **at least three ciphers** from the menu and encrypt a simple message:

Example plaintext:

```
HELLO WORLD
```

For each cipher:

1. Encrypt the message
2. Decrypt it back to plaintext
3. Capture the outputs (screenshot or copy/paste)

---

## **Step 3 — Experiment With Keys**

Try changing:

* Shift amounts (Caesar)
* Keywords (Vigenère)
* 2×2 or 3×3 matrices (Hill)
* Playfair digraph rules

Observe:

* How outputs change
* Whether padding characters like **X** appear
* How the structure of the cipher affects complexity

---

## **Step 4 — Try Attacks and Weakness Testing**

Use the toolkit or your own reasoning to examine weaknesses:

* **Brute force** the Caesar cipher
* Try to break patterns in Vigenère
* Notice how Atbash needs *no key*
* Observe how Rail Fence leaks patterns

Reflect on:

> Why are these ciphers easy to break today?

---

## **Step 5 — Document Your Findings**

You will produce a short report summarizing:

* Three ciphers you explored
* Your encryption/decryption results
* What you learned about each cipher
* Strengths and weaknesses
* Why modern cryptography replaces them

---

# 📤 **What to Submit**

Submit a **short report** (Word, PDF, or Markdown) containing:

* Your name and course section
* Screenshots of toolkit outputs
* Plaintext → Ciphertext → Decrypted text
* Notes on strengths and weaknesses of each cipher
* 1–2 sentences comparing classical and modern encryption

---

# 📘 **Grading Criteria (20 points)**

| Criterion                 | Points | Description                                                                |
| ------------------------- | ------ | -------------------------------------------------------------------------- |
| **Cipher Exploration**    | 5      | Tested at least 3 ciphers with clear screenshots/results                   |
| **Accuracy of Results**   | 5      | Encryption/decryption outputs make sense and match expected behavior       |
| **Analysis & Reflection** | 7      | Clear explanation of strengths/weaknesses and why these ciphers fail today |
| **Presentation Quality**  | 3      | Well-organized, readable report with labels and explanations               |

---

# 🎓 **Learning Outcomes**

By completing this lab, you will be able to:

* Apply multiple classical ciphers to encrypt and decrypt data
* Compare the structure and security of substitution vs. transposition ciphers
* Identify vulnerabilities such as brute force and frequency analysis
* Explain why modern encryption algorithms are necessary and more secure

---

# 📊 **Example Report Format**

| Cipher   | Plaintext   | Encrypted   | Decrypted   | Notes                                               |
| -------- | ----------- | ----------- | ----------- | --------------------------------------------------- |
| Caesar   | HELLO       | KHOOR       | HELLO       | Easy to brute-force; only 25 key options            |
| Atbash   | HELLO WORLD | SVOOL DLIOW | HELLO WORLD | No key needed; substitution pattern fixed           |
| Vigenère | HELLO       | RIJVS       | HELLO       | Stronger than Caesar; cracked with Kasiski analysis |

---

# ⚠️ **Academic Integrity & Ethical Use**

* This toolkit is for **learning only**.
* These ciphers should **not** be used to secure real data.
* Your submitted work must be **your own**.
* Discussions are allowed, but copying answers is not.

---

Just tell me!
