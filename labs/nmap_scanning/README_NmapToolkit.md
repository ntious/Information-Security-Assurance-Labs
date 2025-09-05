Perfect 👌 — here’s the updated **README\_NmapToolkit.md** with your requested caution block added right after the **Features** section, and attribution at the bottom.

---

````markdown
# 🧰 Nmap Teaching Toolkit (Terminal)

An instructor-friendly, student-ready CLI wrapper for **Nmap** that streamlines common scans into a simple menu. Perfect for labs where students spend more time **observing results** than **typing flags**.

> ⚠️ **Legal/Ethical**: Only scan systems you **own** or have **explicit permission** to test.

---

## ✅ Features
- Checks if **Nmap** is installed; offers to install via apt/dnf/yum/pacman, Homebrew, Chocolatey, or winget.
- Single-target scans with **basic**, **intermediate**, and **advanced** profiles.
- Smart choice between **SYN** (`-sS`) and **TCP connect** (`-sT`) based on privileges.
- Prints results to the terminal, then asks to **save to .txt** (timestamped default filename).
- Cross-platform: Linux, macOS, Windows.

---

## ⚠️ Caution / Disclaimer
This toolkit is provided **strictly for educational purposes**.  
- Only run scans against your **own machines**, **lab virtual machines (VMs)**, or networks where you have **explicit authorization**.  
- **Do not** scan external systems, university networks, or third-party services without written permission. Unauthorized scanning can be considered a **cybersecurity offense** and may violate institutional policies or local laws.  
- Instructors are encouraged to restrict usage to **isolated lab environments** or controlled classroom networks.  

Use responsibly, and always follow **ethical hacking and security research guidelines**.  

---

## 🔧 Requirements
- Python 3.8+
- Nmap (the tool will help you install if missing)

---

## 🚀 Quick Start
```bash
# Make executable (Linux/macOS)
chmod +x nmap_toolkit.py

# Run
python3 nmap_toolkit.py
# or
./nmap_toolkit.py
````

On Windows (PowerShell):

```powershell
python .\nmap_toolkit.py
```

---

## 🧪 Scan Profiles

1. **Quick TCP (top 1000)** – `-sS/-sT -T3`
2. **Default scripts + versions** – `-sC -sV -T4`
3. **Full TCP (all ports)** – `-p- -T4`
4. **Service/Version only** – `-sV -T4`
5. **OS detection** – `-O -T4` *(best with admin/root)*
6. **Aggressive** – `-A -T4` *(scripts + OS + versions)*
7. **UDP top 100 (slow)** – `-sU --top-ports 100 -T4`
8. **Custom flags** – you provide the Nmap switches

> **Note:** Some scans (e.g., `-O`, `-sS`) may require admin/root privileges.

---

## 📝 Saving Results

After each scan you’ll be prompted to save output. Press **Enter** to accept the default timestamped filename, or type your own (e.g., `scan_lab1_targetA.txt`).

---

## 🛡️ Troubleshooting

* **Permission errors**: Re-run with `sudo` (Linux/macOS) or an **Administrator** PowerShell (Windows).
* **Command not found**: Re-run the tool; it will offer an installation path for your OS.
* **Slow scans**: UDP and full-port scans are naturally slower. Adjust timing (`-T3/-T4`) via **Custom flags**.

---

## 👩🏽‍🏫 Instructor Tips

* Pre-share a short **target list** students are allowed to scan (e.g., lab VMs).
* Pair this toolkit with a worksheet: “Predict → Scan → Compare → Explain” for each profile.
* Encourage students to try **Custom flags** after the guided run.

---

## 📄 License

MIT (educational use encouraged)

---

## ✍️ Attribution

Designed by **I. K. Nti**

```

