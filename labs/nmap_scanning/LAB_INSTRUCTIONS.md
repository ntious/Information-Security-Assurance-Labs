# 🔍 Lab: Nmap Scanning Toolkit

## 🎯 Objective
The purpose of this lab is to help students **understand and practice different types of network scans using Nmap** in a safe and controlled way.  
Instead of manually typing every command, this toolkit provides a **menu-driven interface** to quickly run **basic, intermediate, and advanced scans** while still learning the meaning of each option.

This lab supports the course learning outcomes:  
👉 **Identify threats and vulnerabilities associated with open ports and network services.**  
👉 **Apply scanning techniques ethically within authorized environments.**

---

## 📖 Background
Nmap (Network Mapper) is one of the most widely used tools in cybersecurity for:
- **Port Scanning** – discovering open ports on a host  
- **Service Enumeration** – identifying what services are running and their versions  
- **OS Fingerprinting** – estimating the target’s operating system  
- **Scripting Engine** – detecting known vulnerabilities with prebuilt scripts  

⚠️ **Important:** Scanning networks you do not own or do not have permission to test is **illegal**. For this lab, you will only scan:  
- Your **own virtual machines (VMs)**,  
- The **lab sandbox environment** provided, or  
- A **self-hosted system on your private network**.  

---

## 🛠️ Prerequisites
* Python 3.8+ installed  
* Nmap installed (the toolkit will help install if missing)  
* Access to a **VM or local machine** you are authorized to scan  

---

## 📝 Tasks
### Step 1 – Launch the Toolkit
```bash
python3 nmap_toolkit.py
````

### Step 2 – Enter Target

* Enter the IP address of your target VM or self-hosted machine.
  Example: `192.168.1.10`

### Step 3 – Choose Scan Profile

Select from the menu:

1. Quick TCP (top 1000 ports)
2. Default scripts + versions
3. Full TCP (all ports)
4. Service/version only
5. OS detection
6. Aggressive scan (OS + scripts + versions)
7. UDP top 100 ports (slower)
8. Custom flags (enter your own options)

### Step 4 – Observe and Save Results

* Review the results printed in the terminal.
* When prompted, choose to save the output as a text file (e.g., `scan_lab1_targetA.txt`).

---

## 📊 Deliverables

Submit the following in your group folder:

1. **Saved scan result file(s)** for at least **two different profiles** (e.g., Quick TCP + OS Detection).
2. A short **summary table**:

   * Target IP
   * Open ports found
   * Services identified
   * OS detection result (if applicable)

---

## 🤔 Reflection Questions

1. What differences did you notice between a **Quick Scan** and a **Full TCP Scan**?
2. Why might **UDP scans** be slower and less reliable than TCP scans?
3. How does OS detection work, and why might it fail sometimes?
4. Why is it important to run these scans only on authorized networks?

---

## 🛡️ Safety & Ethics

* Only scan systems you are authorized to test.
* Always document and explain what you find—**do not exploit** services or vulnerabilities.
* Treat this lab as practice for professional penetration testing in a responsible way.

---

## ✍️ Attribution

Lab instructions prepared by **I. K. Nti**

