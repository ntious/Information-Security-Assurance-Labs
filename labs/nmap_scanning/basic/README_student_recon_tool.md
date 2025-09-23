# 🛡️ Student Network Recon Tool (Freshman‑Friendly)

This simple Python tool helps you **analyze security threats and vulnerabilities through network reconnaissance**, based on your course module. It provides a **menu** so you can choose what to do, and it **summarizes** Nmap results for you in plain language.

> ⚠️ **Only scan systems you own or have written permission to test.** Unauthorized scanning can be illegal and against university policy.

---

## ✅ What the tool can do

- **Ping** a target (connectivity test)
- **DNS lookup** (using `nslookup` or `dig` if available)
- **WHOIS** (domain registration info)
- **Traceroute/Tracert** (see the network path)
- **Nmap scans** (quick/top ports, service version `-sV`, OS detect `-O`, top UDP, ACK firewall check, traceroute+version)
- **Summaries**: Parses the Nmap XML output and creates beginner‑friendly notes about **open ports, services, and basic risk hints**.

All outputs are saved in a **timestamped folder** in your current directory. Example files you’ll see:

```
recon_results_YYYYMMDD_HHMMSS/
├─ TARGET.txt
├─ TOOLS_CHECK.json
├─ ping.txt
├─ dns_nslookup.txt (or dns_dig.txt)
├─ whois.txt
├─ traceroute.txt or tracert.txt
├─ nmap_quick.txt / nmap_quick.xml
├─ SUMMARY_nmap_quick.md
└─ ... (other tasks you run)
```

---

## 🧰 Requirements

- **Python 3.8+**
- Some external tools (install if missing):
  - **Nmap**: https://nmap.org/download.html
  - **WHOIS**: Often included on Linux/macOS (`brew install whois` on mac). On Windows, use WSL or a whois utility.
  - **Traceroute/Tracert**: Built‑in on most systems (`tracert` on Windows, `traceroute` on macOS/Linux).
  - **nslookup** is usually available; **dig** is a nice alternative if installed.

> The script checks what’s on your PATH and saves a `TOOLS_CHECK.json` so you know what’s available.

---

## 🚀 How to run

1. Download `student_recon_tool.py` to a folder you can find.
2. Open a terminal/shell in that folder.
3. Run:

### Windows (PowerShell)
```powershell
python .\student_recon_tool.py
```

### macOS / Linux
```bash
python3 ./student_recon_tool.py
```

4. **Read the ethics notice** and confirm you have permission.
5. Enter a **target** (domain like `example.com` or IP like `8.8.8.8`).
6. Choose from the **menu** (1–13). Use option **12** for a safe, beginner bundle.

---

## 📘 Tips for Freshmen

- Start with **Ping** and **DNS** to understand connectivity and names.
- Run the **Quick Nmap scan** to see common open ports.
- Use **Service Version** (`-sV`) to learn what software is behind a port.
- The **Summaries** (`SUMMARY_*.md`) explain what you found in simple terms.
- When in doubt, ask your instructor/TA or visit the IT Learning Center.

---

## 🧪 Example learning questions

- Which ports are open on your approved test host?
- What services and versions are running? Any that should be disabled (e.g., Telnet)?
- How many network “hops” does traceroute show to the target?
- Does WHOIS show when the domain was created or who owns it?

---

## 🔐 Ethics & Safety

- **Never** scan random or unauthorized systems.
- Respect **rate limits** and don’t use aggressive options against production systems.
- When writing reports, avoid sharing sensitive data publicly.

---

## ❓ Troubleshooting

- **Nmap not found**: Install it and reopen your terminal so PATH updates.
- **WHOIS not found**: Install a whois package (or use WSL on Windows).
- **Permission denied** (OS detection): Some scans need elevated privileges (e.g., raw sockets). Try running your terminal as **Administrator** (Windows) or with `sudo` (macOS/Linux) *only if permitted*.

---

## 📄 License

MIT — free to use for coursework.

---

### 👩🏽‍🏫 For Instructors (optional)

- The script produces standardized outputs for easy grading.
- Students can ZIP the `recon_results_*` folder and submit.
- Summaries are intentionally simple and beginner‑friendly.
