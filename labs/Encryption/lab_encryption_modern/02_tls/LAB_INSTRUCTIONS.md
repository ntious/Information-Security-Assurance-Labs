# Lab: TLS/SSL in Practice
## 🎯 Objective
The purpose of this lab is to help students **understand how TLS (Transport Layer Security) works** by inspecting real-world certificates and running a local TLS echo server.  
You will learn how **certificates, ciphers, and protocols** protect communication over the internet.
---
## 📖 Background
TLS (successor of SSL) is the backbone of secure internet communication. It provides:
- **Encryption** – prevents eavesdropping  
- **Authentication** – verifies the identity of servers/clients  
- **Integrity** – ensures data has not been tampered with  

Certificates, issued by trusted Certificate Authorities (CAs), play a crucial role.  

Here, we’ll use **OpenSSL** to inspect live websites and generate our own **self-signed certificates** for practice.

This activity supports the course learning outcome:  
👉 **Explain the role of SSL/TLS in securing communications.**
---
## 🛠️ Prerequisites
* GitHub Codespaces (OpenSSL and Python preinstalled via `.devcontainer`)  
* Basic knowledge of networking and HTTPS  
---
## 📝 Tasks
### Step 1 – Inspect a Public TLS Certificate
1. Run:
   ```bash
   openssl s_client -connect example.com:443 -servername example.com -showcerts </dev/null
Identify:
* TLS version
* Cipher suite
* Certificate subject (who it’s issued to)
* Certificate issuer (who signed it)
* Validity dates
---
### Step 2 – Create a Self-Signed Certificate
1.	Navigate to the lab folder:

cd labs/Encryption/lab_encryption_modern/02_tls
Run:
bash make_self_signed.sh

This generates cert.pem and key.pem.
---
### Step 3 – Run a TLS Echo Server
Start the server:
Run:
make tls-run

Open a second terminal and connect:
Run:
openssl s_client -connect localhost:4443 -servername localhost </dev/null

Type a message — the server should echo it back.
---
### 📂 Deliverables
A short report including:
* TLS details from inspecting a real website (screenshot or copy-paste)
* Evidence of successful certificate creation (subject, issuer, dates)
* Screenshot of a TLS echo session working locally
* Reflection: Why do browsers trust some certificates and not others?
---
### ✅ Evaluation Criteria
* Completion – Certificate inspection + echo server demonstrated
* Accuracy – Correct identification of TLS details
* Analysis – Explanation of certificate trust and TLS role
* Presentation – Clear, structured report with screenshots
---
### 📘 Learning Outcomes
* By completing this lab, you will be able to:
* Inspect and interpret TLS certificates
* Generate and use self-signed certificates
* Explain how TLS secures communications
* Recognize the importance of certificate authorities
---
### ⚠️ Ethical Reminder
- Only inspect public websites you are authorized to connect to.
- Do not attempt to intercept or tamper with real traffic.
- This lab is for educational purposes only.
---