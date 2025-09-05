# Lab: VPN Concepts – WireGuard & OpenVPN

## 🎯 Objective

The purpose of this lab is to help students **understand how VPNs (Virtual Private Networks) secure communications**.  
You will analyze example WireGuard and OpenVPN configuration files and compare VPNs to TLS/SSH.

---

## 📖 Background

VPNs establish **encrypted tunnels** between endpoints, often at the network layer.  
They are widely used for:

- Secure remote work connections  
- Protecting traffic on public Wi-Fi  
- Bypassing geo-restrictions  

Two common protocols:
- **WireGuard** – modern, lightweight, simple configs  
- **OpenVPN** – widely used, flexible, works across platforms  

This activity supports the course learning outcome:  
👉 **Explain the role of VPNs in securing communications.**

---

## 🛠️ Prerequisites

* GitHub Codespaces (analysis only; no tunnel setup needed)  
* Basic networking knowledge  

---

## 📝 Tasks

### Step 1 – Explore WireGuard Config
Open `wireguard_example.conf` and identify:
- Private key  
- Peer’s public key  
- Endpoint  
- Allowed IP ranges  

---

### Step 2 – Explore OpenVPN Config
Open `openvpn_client_example.ovpn` and identify:
- Remote server  
- Cipher and authentication methods  
- Certificates and keys used  

---

### Step 3 – Compare with TLS & SSH
Write a short paragraph comparing:
- VPN vs TLS (different layers, scope of protection)  
- VPN vs SSH (use cases, tunneling vs login security)

---

## 📂 Deliverables

* A short **report** including:
  * Notes on WireGuard config (explain at least 3 fields)  
  * Notes on OpenVPN config (explain at least 3 fields)  
  * Comparison of VPN vs TLS vs SSH  
* Reflection: Why would an organization use a VPN in addition to TLS and SSH?

---

## ✅ Evaluation Criteria

* **Completion** – Both config files analyzed  
* **Accuracy** – Correct interpretation of key fields  
* **Analysis** – Clear comparison of VPN vs TLS vs SSH  
* **Presentation** – Well-structured and concise report  

---

## 📘 Learning Outcomes

By completing this lab, you will be able to:

* Explain the purpose of VPNs in secure communication  
* Identify common config fields in WireGuard and OpenVPN  
* Compare VPNs to TLS and SSH in real-world usage  

---

## ⚠️ Ethical Reminder

Do not attempt to set up or connect to unauthorized VPNs.  
These configs are **examples only**.  
This lab is for **educational purposes only**.