# INSTRUCTOR NOTES – Classical Ciphers Toolkit Lab

This document is for **instructor use only**.  
It explains how to use `classical_ciphers_toolkit.py` effectively in class, how the lab aligns with course outcomes, and how to support students during the activity.

---

## 1. Lab Overview

**Lab Title:** Exploring Classical Encryption  
**Tool:** `classical_ciphers_toolkit.py` (all-in-one menu-driven Python script)

Students use the toolkit to:

- Encrypt and decrypt messages using **multiple classical ciphers**
- Experiment with **keys** (shifts, keywords, matrices, rails)
- Perform **brute-force and auto-decrypt** attacks (Caesar)
- Reflect on the **strengths and weaknesses** of each cipher

This lab is intentionally **conceptual + hands-on**. Students do not need deep Python skills; they mainly interact via the menu and prompts.

---

## 2. Course & Module Alignment

### Course Learning Outcomes Supported

- **Describe the history of information technology and its associated disciplines.**  
  Classical ciphers give a concrete historical anchor for early cryptography.

- **Identify and explain the specialty areas and basic concepts of information technology.**  
  Introduces students to **information security** and **cryptography** as core IT areas.

- **Apply introductory skills and concepts related to digital media, web technologies, programming, networking, and systems administration.**  
  Here, students apply **introductory cryptographic concepts** and interact with a Python script.

### Specific Module Objectives Supported

From your encryption/access control module:

- Encrypt and decrypt messages using a key and a **shift cipher** (Caesar).  
- Use **brute force** to solve a cipher without a key (Caesar brute force / auto-decrypt).  
- Recognize and recall **terminology related to encryption**, symmetric ciphers, and simple cryptanalysis.  
- Begin to distinguish **classical vs. modern encryption** (conceptual bridge to AES/RSA later).

---

## 3. Files & Structure

Recommended lab folder structure:

- `classical_ciphers_toolkit.py`  
- `LAB_INSTRUCTIONS.md` (student-facing)  
- `INSTRUCTOR_NOTES.md` (this file)  

Optional:

- `examples/` – with sample plaintext/ciphertext pairs  
- `solutions/` – if you want to keep sample outputs separate

---

## 4. How to Demo the Toolkit in Class

### A. Quick Setup

From the lab folder:

```bash
python classical_ciphers_toolkit.py
