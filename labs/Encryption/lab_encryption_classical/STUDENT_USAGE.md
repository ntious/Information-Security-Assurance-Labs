# **STUDENT_USAGE.md**

### *How to Use This Repository for the Classical Encryption Lab*

Welcome to the **Information Security Assurance Labs** repository!
This guide explains **exactly how to use the materials in the `lab_encryption_classical` folder** to complete your lab on Classical Cryptography.

Follow these steps, and you will be able to run the toolkit, execute the tasks, take screenshots, and finish the lab **without needing any additional clarification**.

---

# 📁 **1. Locate the Correct Lab Folder**

All files for this lab are inside:

```
Information-Security-Assurance-Labs/labs/Encryption/lab_encryption_classical
```

Inside this folder you will see:

* `classical_ciphers_toolkit.py` ← **MAIN program to run**
* `README.md` ← Overview & instructions
* `CLASSICAL_CIPHERS_NOTES.md` ← History + explanations of all ciphers
* `LAB_INSTRUCTIONS.md` ← Step-by-step lab tasks (same as Canvas)
* `INSTRUCTOR_NOTES.md` ← Ignore this (for instructors only)
* `requirements.txt` ← Dependencies for local setup

---

# 🧰 **2. Running the Toolkit (Two Options)**

## **OPTION A — Run on Your Laptop (Local Setup)**

Use this if you have Python installed.

### **Requirements**

* Python **3.7+**
* NumPy installed

Install NumPy:

```bash
pip install numpy
```

### **Run the toolkit**

1. Open your terminal.
2. Navigate to the lab folder.

   ```bash
   cd Information-Security-Assurance-Labs/labs/Encryption/lab_encryption_classical
   ```
3. Run the program:

   ```bash
   python classical_ciphers_toolkit.py
   ```

You should now see:

```
=== Classical Ciphers Toolkit ===
1 - Caesar | 2 - Atbash | 3 - Affine | 4 - Vigenere
5 - Rail Fence | 6 - Columnar | 7 - Playfair | 8 - Hill
9 - Autokey | 10 - Beaufort | 11 - Hybrid | Q - Quit
```

---

## **OPTION B — Use Binder (Cloud Environment — No Installation Required)**

If you do **NOT** have Python installed, use Binder.

### **Steps**

1. Go to the repo folder on GitHub.
2. Click the **Launch Binder** button.
3. Wait for Binder to load (may take 30–60 seconds).
4. Click **View → Open in JupyterLab**.
5. On the left panel, open:

```
labs → Encryption → lab_encryption_classical
```

6. Open a terminal (top left: *File → New → Terminal*).
7. Install NumPy:

   ```bash
   pip install numpy
   ```
8. Run:

   ```bash
   python classical_ciphers_toolkit.py
   ```

---

# 🔐 **3. Using the Toolkit**

Each cipher has its own menu with:

* **E** – Encrypt
* **D** – Decrypt
* **B** – Brute Force (Caesar only)
* **A** – Auto-Decrypt (Caesar only)

Follow the prompts exactly as shown in the terminal.

**Important:** Some ciphers remove spaces or add padding (e.g., `X`).
This is expected and part of classical cipher behavior.

---

# 📝 **4. Completing Your Lab Tasks**

Your Canvas assignment corresponds *exactly* to the toolkit functions.
You will:

✔ Encrypt plaintext
✔ Decrypt ciphertext
✔ Brute-force Caesar
✔ Try multiple keys for Vigenère
✔ Explore two additional ciphers of your choice
✔ Generate MD5 & SHA-1 hashes using a website
✔ Take screenshots for all results

Everything you need to complete Tasks 1–7 is already in this folder.

---

# 📸 **5. Taking Screenshots**

Every screenshot must show:

* The cipher menu
* Your input
* The result (encrypted or decrypted text)

Screenshots must be placed into your final submission document for Canvas.

---

# 📚 **6. Reading Material (Optional but Recommended)**

Before starting your lab, read:

### **`README.md`**

Gives you a full overview of the toolkit.

### **`CLASSICAL_CIPHERS_NOTES.md`**

Explains:

* How each cipher works
* Historical background
* Strengths & weaknesses

This will help you answer reflection questions.

---

# 🆘 **7. If You Get Stuck**

Before asking the instructor, check:

✔ Are you using the correct folder?
✔ Did you install NumPy?
✔ Did you type your key exactly as required (case doesn’t matter)?
✔ Did you remove spaces when required (Columnar, Hill, Playfair)?

Most errors come from copy/paste formatting—**type text manually if needed**.

---

# 📝 **8. Submitting Your Work**

Submit **one PDF or Word document** containing:

* All tasks (1–7)
* **Nine** screenshots (labelled)
* Ciphertexts, plaintexts, and keys used
* Hash results & integrity explanation
* Reflection questions

---

# 🎓 **You Are Ready to Begin**

This guide prepares you fully to use the repo and complete the Classical Ciphers Lab independently.

