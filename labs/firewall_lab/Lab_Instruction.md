# 🔒 Lab: Firewall Configuration with UFW

## 🎯 Objective
The purpose of this lab is to help students **understand how host-based firewalls protect services** from unauthorized access and attacks.  
You will use **UFW (Uncomplicated Firewall)** on Ubuntu to configure rules, test services, and verify that security policies are enforced.

This activity supports the course learning outcome:  
👉 **Implement and verify basic access control using firewall policies.**

---

## 📖 Background
Firewalls are a critical first line of defense. They:
- Restrict access to services by **port** or **protocol**
- Limit access to trusted **IP addresses**
- Enforce **default deny** rules so only explicitly allowed traffic gets through

**UFW** is a user-friendly front end for `iptables` that simplifies firewall management on Ubuntu.

---

## 🛠️ Prerequisites
- Ubuntu VM (University Sandbox or local Ubuntu installation)  
- Sudo access on the machine  
- Internet connection  
- Installed tools:
  ```bash
  sudo apt update
  sudo apt install -y ufw curl netcat-openbsd openssl python3
````

---

## 📝 Tasks

### Step 1 – Check Network Info

```bash
ip addr
ss -tulpen
```

👉 Record your IP address and any listening ports.

---

### Step 2 – Verify Firewall Status

```bash
sudo ufw status verbose
```

Expected: `Status: inactive` on a new VM.

---

### Step 3 – Enable Firewall

```bash
sudo ufw enable
```

⚠️ This may warn that it could disrupt SSH connections. Since we will allow SSH next, it is safe.

---

### Step 4 – Set Default Policies

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

This ensures a **default deny** stance.

---

### Step 5 – Allow Trusted Ports

* Allow SSH (22), HTTP (80), and HTTPS (443):

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

### Step 6 – Deny Insecure Ports

* Deny FTP (21) and Telnet (23):

```bash
sudo ufw deny 21/tcp
sudo ufw deny 23/tcp
```

---

### Step 7 – Configure IP-Based Rules

* Allow SSH only from a trusted IP:

```bash
sudo ufw allow from 192.168.1.100 to any port 22
```

* Block all traffic from a malicious IP:

```bash
sudo ufw deny from 203.0.113.1
```

---

### Step 8 – Verify Rules

```bash
sudo ufw status numbered
sudo ufw status verbose
```

👉 Take a screenshot of your rules.

---

### Step 9 – Test with Services

1. Start a test HTTP server:

   ```bash
   python3 -m http.server 8000
   ```
2. Start a simple HTTPS server:

   ```bash
   openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 1 -nodes -subj "/CN=localhost"
   python3 - <<'PY'
   ```

import http.server, ssl, socketserver
handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", 8443), handler) as httpd:
httpd.socket = ssl.wrap\_socket(httpd.socket, server\_side=True, certfile="cert.pem", keyfile="key.pem")
print("Serving HTTPS on 8443")
httpd.serve\_forever()
PY

````

3. Test access:
```bash
curl http://<your-ip>:8000
curl -k https://<your-ip>:8443
nc -vz <your-ip> 21    # should be blocked
nc -vz <your-ip> 80    # should succeed
````

---

## ✅ Deliverables

Submit the following:

1. Screenshot of `ufw status verbose` showing correct rules:

   * Default deny incoming / allow outgoing
   * ALLOW 22, 80, 443
   * DENY 21, 23
2. Evidence of testing with `curl`/`nc`:

   * HTTP and HTTPS succeed
   * FTP/Telnet blocked
3. (Optional) Evidence of IP-based rule test
4. Run the checker:

   ```bash
   bash ufw_check.sh
   ```

   Include the checker output in your submission.

---

## ⚡ Reflection Questions

1. Why is a **default deny** policy considered best practice?
2. What risks are introduced by leaving ports like **21** and **23** open?
3. How does IP-based allow/deny improve security? What are its limitations?
4. In real-world enterprise setups, would this firewall configuration be sufficient? Why or why not?

---

## 🔑 Key Takeaways

* Firewalls enforce the principle of **least privilege**.
* Always start with **default deny**, then allow only what’s needed.
* Combine **port-based rules** with **IP-based restrictions** for stronger security.
* Testing is critical—firewall rules are only as good as the verification steps that prove they work.

```