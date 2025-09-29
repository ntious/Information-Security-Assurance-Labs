# Netstat Lab Helper — Package

This package contains:
- `netstat_lab_helper.py` — updated menu-driven helper for Tasks 2–4
- `Task4_Reflection_Template.docx` — a fill‑in reflection doc
- This README

## How to run
```bash
# if netstat is missing
sudo apt update && sudo apt install -y net-tools

# recommended to see PIDs/program names
sudo -E python3 netstat_lab_helper.py
```

## Notes
- Option 2 now checks ports **3306** and **33060** and includes a **deep hunt** for
  LISTEN + UNIX sockets, so you always have something useful to document.
- If you see no TCP entries, MySQL may be **UNIX-socket only**. Use the deep hunt
  output or open a TCP client (`mysql -h 127.0.0.1 -P 3306 -u root -p`) and re-check.