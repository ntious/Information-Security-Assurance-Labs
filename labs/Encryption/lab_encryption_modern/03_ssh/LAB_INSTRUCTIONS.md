# Lab: SSH Keys & Secure Remote Access

## 🎯 Objective
The purpose of this lab is to help students **understand how SSH secures remote logins and file transfers**.  
You will generate keypairs, verify host fingerprints, and connect securely to GitHub using SSH.

---

## 📖 Background
SSH (Secure Shell) provides encrypted remote access. It uses:

- **Public key authentication** – private key proves identity, public key is shared  
- **Host key verification** – prevents man-in-the-middle attacks  
- **Encryption** – keeps commands and files private  

This activity supports the course learning outcome:  
👉 **Explain the role of SSH in securing communications.**

---

## 🛠️ Prerequisites
- GitHub Codespaces (with `ssh` client installed)  
- GitHub account  

---

## 📝 Tasks

### Step 1 – Generate SSH Keys
Run:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/student_key -C "student@example.com"
````

This creates:

* `~/.ssh/student_key` (private key)
* `~/.ssh/student_key.pub` (public key)

---

### Step 2 – Add Public Key to GitHub

Copy your public key:

```bash
cat ~/.ssh/student_key.pub
```

Then add it to GitHub under:
**Settings → SSH and GPG keys → New SSH key**

---

### Step 3 – Verify GitHub Host Key

Run:

```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

This saves GitHub’s host fingerprint locally.

---

### Step 4 – Test SSH Authentication

Run:

```bash
ssh -i ~/.ssh/student_key -T git@github.com
```

You should see a message like:

> “Hi student! You’ve successfully authenticated…”

---

## 📂 Deliverables

Submit a short **report** including:

* Screenshot of SSH key generation
* Public key snippet added to GitHub
* Screenshot of successful GitHub SSH connection
* Reflection: Why are SSH keys more secure than passwords?

---

## ✅ Evaluation Criteria

* **Completion** – Keypair generated, GitHub key added, SSH test successful
* **Accuracy** – Correct handling of public vs private keys
* **Analysis** – Clear explanation of SSH’s role in secure communication
* **Presentation** – Screenshots + explanations are neat and clear

---

## 📘 Learning Outcomes

By completing this lab, you will be able to:

* Generate and manage SSH keypairs
* Explain the purpose of host key verification
* Connect to GitHub securely using SSH
* Compare SSH to TLS in terms of use cases and trust models

---

## ⚠️ Ethical Reminder

* Never share your **private key**.
* Only use SSH to connect to **authorized systems**.
* This lab is for **educational purposes only**.

```


