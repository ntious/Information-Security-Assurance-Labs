Perfect ✅ To keep it consistent with your other labs, here’s a **`LAB_INSTRUCTIONS.md`** for your **Classical Encryption Lab**.

Save this inside:
`labs/lab_encryption_classical/LAB_INSTRUCTIONS.md`

---

# Lab: Exploring Classical Encryption

## 🎯 Objective

The purpose of this lab is to help students **understand and experiment with classical ciphers**. By using a Python toolkit, you will encrypt, decrypt, and analyze text with **11 major historical ciphers**, gaining hands-on experience with substitution and transposition techniques.

---

## 📖 Background

Cryptography has evolved over centuries. Early systems like Caesar or Vigenère were once effective but are now easy to break with modern computing. Studying these classical ciphers provides valuable insight into the **principles of encryption, weaknesses of simple systems, and the evolution toward modern cryptography**.

This activity supports the course learning outcome:
👉 **Identify and apply cryptographic techniques to secure information.**

---

## 🛠️ Prerequisites

* Python **3.7+**
* `numpy` library (for Hill cipher math)

  ```bash
  pip install numpy
  ```
* Basic understanding of substitution and transposition concepts

---

## 📝 Tasks

### Step 1 – Run the Toolkit

* Open a terminal and run:

  ```bash
  python classical_ciphers_toolkit.py
  ```
* Explore the menu of ciphers.

### Step 2 – Encrypt and Decrypt Messages

* For each cipher, try encrypting and decrypting a short message (e.g., `"HELLO WORLD"`).
* Record your results.

### Step 3 – Experiment with Keys

* Change keys (shifts, matrices, or keywords) and observe how outputs change.
* Note how some ciphers (e.g., Playfair, Hill) add padding characters like `X`.

### Step 4 – Analyze Strengths and Weaknesses

* Test brute-force attacks (Caesar, Affine).
* Discuss why some ciphers are easy to break.

### Step 5 – Document Your Findings

* Record results for at least **3 different ciphers**.
* Summarize what makes each cipher strong or weak.

---

## 📂 Deliverables

* A short **report** (Markdown, Word, or PDF) including:

  * Screenshots of encryption/decryption results
  * Example plaintext → ciphertext → recovered plaintext
  * Notes on strengths and weaknesses of at least 3 ciphers

---

## ✅ Evaluation Criteria

* **Completion** – Did you test at least 3 ciphers?
* **Accuracy** – Did your encrypt/decrypt results match expectations?
* **Analysis** – Did you explain why some ciphers are weaker/stronger?
* **Presentation** – Is your report clear, structured, and easy to follow?

---

## 📘 Learning Outcomes

By completing this lab, you will be able to:

* Apply substitution and transposition ciphers in practice
* Compare the effectiveness of different classical ciphers
* Recognize limitations of early cryptographic systems
* Explain why modern encryption is necessary

---

## 📊 Example Report Structure

| Cipher   | Plaintext   | Encrypted   | Decrypted   | Notes                                                       |
| -------- | ----------- | ----------- | ----------- | ----------------------------------------------------------- |
| Caesar   | HELLO       | KHOOR       | HELLO       | Easy to brute-force                                         |
| Atbash   | HELLO WORLD | SVOOL DLIOW | HELLO WORLD | Symmetric, no key needed                                    |
| Vigenère | HELLO       | RIJVS       | HELLO       | Stronger than Caesar, but crackable with frequency analysis |

---

## ⚠️ Ethical Reminder

This toolkit is for **educational purposes only**. These ciphers are outdated and should **never be used for real-world data protection**. The goal is to learn cryptographic fundamentals, not to create secure systems.