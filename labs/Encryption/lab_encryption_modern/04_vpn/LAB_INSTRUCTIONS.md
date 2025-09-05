# Lab: VPN Concepts – WireGuard & OpenVPN

## 🎯 Objective
Understand how VPNs (Virtual Private Networks) secure communications. You will analyze example **WireGuard** and **OpenVPN** configuration files and compare VPNs to **TLS/SSH**.

---

## 📖 Background
VPNs establish **encrypted tunnels** between endpoints (often at the network layer). They’re widely used for:
- Secure remote work connections
- Protecting traffic on public Wi-Fi
- Accessing private/internal resources

Common protocols:
- **WireGuard** – modern, lightweight, simple configs
- **OpenVPN** – widely used, flexible, cross-platform

This activity supports the course learning outcome:  
👉 **Explain the role of VPNs in securing communications.**

---

## 🛠️ Prerequisites
- GitHub Codespaces (analysis only; **no tunnel setup needed**)
- Basic networking knowledge (IP addressing, routing)

---

## 📝 Tasks

### Step 1 — Explore WireGuard Config
Open `wireguard_example.conf` and identify:
- **Interface** address (client’s tunnel IP)
- **PrivateKey** (client secret; never share)
- **Peer/PublicKey** (server identity)
- **Endpoint** (server address:port)
- **AllowedIPs** (what routes through the tunnel)

### Step 2 — Explore OpenVPN Config
Open `openvpn_client_example.ovpn` and identify:
- **remote** (server host/port) and **proto/dev** (transport + tunnel type)
- **cipher/auth** (encryption & HMAC choices)
- **<ca>/<cert>/<key>/<tls-auth>** (trust + client identity + anti-DoS)

### Step 3 — Compare with TLS & SSH
Write a short paragraph comparing:
- **VPN vs TLS:** different layers and scope (network-wide tunnel vs app-level)
- **VPN vs SSH:** tunneling/routing vs interactive login/port-forwarding

---

## 📂 Deliverables
Submit a short report that includes:
- Notes on **WireGuard** (explain ≥3 fields)
- Notes on **OpenVPN** (explain ≥3 fields)
- A comparison of **VPN vs TLS vs SSH**
- **Reflection:** Why might an organization use a VPN in addition to TLS and SSH?

---

## ✅ Evaluation Criteria
- **Completion (30%)** – Both configs analyzed
- **Accuracy (30%)** – Correct interpretation of key fields
- **Analysis (30%)** – Clear comparison (layering, scope, use cases)
- **Presentation (10%)** – Concise, well-structured write-up

---

## 📘 Learning Outcomes
By completing this lab, you will be able to:
- Explain the purpose of VPNs in secure communication
- Identify common config fields in WireGuard and OpenVPN
- Compare VPNs to TLS and SSH in real-world usage

---

## 🔍 Optional Extension (Bonus)
- Propose a **split-tunnel** vs **full-tunnel** policy for a university laptop.  
  Which subnets should be routed via VPN and why? Mention security vs performance trade-offs.

---

## ⚠️ Ethical Reminder
Do not attempt to set up or connect to unauthorized VPNs. These configs are **examples only**.  
This lab is for **educational purposes**.
