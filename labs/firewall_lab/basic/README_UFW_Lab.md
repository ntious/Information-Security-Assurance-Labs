# UFW Firewall Lab Helper (Freshman-Friendly)

This repo contains a Python script to guide freshmen through **Implementing Technical Security Controls – Part 1** using the **UFW firewall** on Ubuntu. It follows the instructor handout and adds menu-driven automation, helpful prompts, and optional advanced tasks.

---

## What You'll Learn
- Check whether the firewall is active
- Enable UFW
- Allow **HTTP (80/tcp)**, **HTTPS (443/tcp)**, and **SSH (22/tcp)**
- Set default policy to **deny incoming**
- **Block** specific ports like **FTP (21/tcp)** and **Telnet (23/tcp)**
- Allow SSH from a **trusted IP** and **block** a malicious IP
- Verify with `curl` (HTTP/HTTPS) and `telnet` or `nc` (blocked port)
- (Advanced, optional) Set UFW logging level, **rate-limit SSH**, **export/restore** rules, and **reset** UFW

> Built to align with your lab slides (Firewall configuration with UFW, allowing/denying ports, IP-based rules, and testing).

---

## Requirements
- Ubuntu-based VM (your course sandbox/VM).
- Python 3.8+.
- UFW installed (`sudo apt update && sudo apt install ufw -y`).
- For actually changing firewall rules, you’ll typically need `sudo` privileges.
- For verification:
  - `curl` (usually pre-installed): `sudo apt install curl -y`
  - `telnet` or `nc` (optional): `sudo apt install telnet -y` or `sudo apt install netcat -y`

> **Tip:** If you’re in an environment without `sudo` (e.g., some Codespaces), use **DRY-RUN** mode to see the commands you should run in a terminal that *does* have permission.

---

## Quick Start
```bash
# 1) Download the script
wget https://example.com/firewall_lab_helper.py -O firewall_lab_helper.py  # or use the file provided by your instructor

# 2) Run it
python3 firewall_lab_helper.py
```

You’ll see a menu with numbered options. Read each description and follow along.

---

## Menu Overview
- **[1] Status** – Shows `ufw status verbose`.
- **[2] Enable UFW** – Turns on UFW if inactive.
- **[3] Allow Common Ports** – Adds rules for 80, 443, and 22 (HTTP, HTTPS, SSH).
- **[4] Default Deny Incoming** – Sets default incoming policy to deny (least privilege).
- **[5] Block Legacy Ports** – Denies 21 (FTP) and 23 (Telnet).
- **[6] Allow SSH from Trusted IP** – Example of narrowing access to a known admin IP.
- **[7] Deny from IP** – Blocks a misbehaving or suspicious IP.
- **[8] Show Numbered Rules** – Useful when deleting rules.
- **[9] Delete by Number** – Removes a rule by its index.
- **[10] Verify HTTP/HTTPS** – Uses `curl` to request headers from your server/IP.
- **[11] Test Blocked Port** – Uses `telnet` or `nc` to demonstrate a blocked service.
- **[12] Toggle DRY-RUN** – If **ON**, commands are printed but not executed.

### Advanced (optional)
- **[13] Logging Level** – `off/low/medium/high/full` (for learning & troubleshooting).
- **[14] Rate-Limit SSH** – Throttles repeated SSH attempts (mitigates brute-force).
- **[15] Export Rules** – Saves `/etc/ufw/user.rules` to a file (needs permission).
- **[16] Restore Rules** – Restores rules from a file and reloads UFW.
- **[17] Reset UFW** – Resets to defaults (⚠️ removes rules). Use with caution.

---

## Sample Walkthrough (Matches Your Lab)
1. **Show status** → confirm UFW is inactive or active.
2. **Enable UFW** if inactive.
3. **Allow** 80/tcp, 443/tcp, and 22/tcp.
4. **Default deny incoming**.
5. **Deny** 21/tcp and 23/tcp.
6. (Optional) **Allow SSH** from a specific trusted IP (e.g., your home/IT network).
7. (Optional) **Deny** a known-bad IP.
8. **Verify** with:
   - `curl -I http://<your-ip>` and `curl -I https://<your-ip>`
   - `telnet <your-ip> 21` (or `nc -vz <your-ip> 21`) → should fail if blocked.

> If your VM doesn’t run a web server, `curl` might show a connection error. That’s okay—focus on whether the **firewall rules** are configured as instructed.

---

## Troubleshooting
- **Permission denied / need sudo:** Run the script with `sudo -E python3 firewall_lab_helper.py` *or* toggle DRY-RUN and copy commands into a terminal with sudo access.
- **telnet/nc not found:** Install with `sudo apt install telnet -y` or `sudo apt install netcat -y`.
- **Not Ubuntu?** Use your course’s Ubuntu VM or WSL on Windows.
- **Locked-down environment?** DRY-RUN to learn commands without applying changes.

---

## Why These Steps Matter (Security Rationale)
- **Allow only what you need** (HTTP/HTTPS/SSH) and **deny by default** to reduce attack surface.
- **Block old/unsafe services** (FTP/Telnet) to prevent credential sniffing and legacy protocol abuse.
- **Restrict SSH by source IP** as a simple hardening step.
- **Rate-limit SSH + logging** help detect & slow brute-force attacks.

---

## Acknowledgment
This helper aligns with your lab slides on **Technical Security Controls** for Ubuntu UFW (allow/deny ports, IP-based rules, and verification tests).

---

## License
For educational use in your course.
