#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
netstat_lab_helper.py — Menu-Driven Helper (Updated)
=======
netstat_lab_helper.py — Menu-Driven Helper
>>>>>>> f49c36459c093bb9b27aafdad1a239785737a739
=====================================================================
Supports Task 2–4 of the "Network Statistics Using netstat" lab.
Adds deeper MySQL detection (TCP 3306/33060 + UNIX sockets) and
guidance for running with sudo when PIDs are hidden.

<<<<<<< HEAD
Run with sudo for full visibility:
    sudo -E python3 netstat_lab_helper.py
=======
⚠️ ETHICS, SAFETY, AND CLASSROOM CONTEXT
---------------------------------------------------------------------
• Only run this on your **UC Sandbox Ubuntu VM** for this course.
• Do NOT scan or kill processes on machines you do not own or manage.
• Killing the wrong PID can disrupt services; confirm before proceeding.

WHAT THIS SCRIPT DOES
---------------------------------------------------------------------
1) Detects whether **netstat** (net-tools) or **ss** (modern replacement) is
   available. Uses whichever is present. (The lab mentions netstat; if it's
   missing, this tool will transparently use ss.)
2) Lists **active TCP/UDP connections** with process IDs (PIDs).
3) Filters for **MySQL-related** connections (default port 3306) and tries to
   show likely PIDs for the containerized MySQL service.
4) Saves connection snapshots to timestamped text files in `lab_outputs/` to
   help you collect **screenshot alternatives** and attach to your report.
5) Provides a guided **kill-by-PID** workflow with confirmation prompts.
6) Generates a **Reflection Template (Task 4)** you can fill in and submit.

QUICK START (Typical Flow for Task 2–3)
---------------------------------------------------------------------
1) Option 1 or 2: View active connections (all / MySQL-focused).
2) Option 4: Save a snapshot of the current connections for your report.
3) Option 5: If instructed, terminate a malicious MySQL PID (with caution).
4) Option 6: Generate the reflection template for Task 4 and fill it in.

REQUIREMENTS
---------------------------------------------------------------------
• Python 3.8+
• Ubuntu VM in Sandbox.
• "netstat" (net-tools) or "ss" available on the VM. If netstat is missing,
  install net-tools with:    sudo apt update && sudo apt install -y net-tools

NOTES FOR SCREENSHOTS
---------------------------------------------------------------------
• This script saves outputs under ./lab_outputs with timestamps. You can
  screenshot either the terminal output or include the saved text files in your
  Word/PDF report.

Author: Your Course Team
Version: 1.0
License: MIT (for classroom use)
>>>>>>> f49c36459c093bb9b27aafdad1a239785737a739
"""
import os
import re
import shlex
import subprocess
from datetime import datetime
from pathlib import Path

# ----------------------------- Utilities -----------------------------
LAB_DIR = Path.cwd()
OUT_DIR = LAB_DIR / "lab_outputs"
OUT_DIR.mkdir(exist_ok=True)

# include X Protocol 33060 as well
MYSQL_DEFAULT_PORTS = {"mysql": (3306, 33060)}

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def pause(msg="\nPress Enter to continue..."):
    try:
        input(msg)
    except EOFError:
        pass

def check_command_exists(cmd: str) -> bool:
    return subprocess.call(
        ["bash", "-lc", f"command -v {shlex.quote(cmd)} >/dev/null 2>&1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ) == 0

# Prefer ss if present; otherwise netstat; else suggest installing net-tools
TOOLS = {
    "ss": {
        "exists": check_command_exists("ss"),
        "cmd_all": "ss -tunap",   # TCP/UDP, numeric, all, with process
        "pretty": "ss (modern replacement for netstat)",
    },
    "netstat": {
        "exists": check_command_exists("netstat"),
        "cmd_all": "netstat -tunap",
        "pretty": "netstat (from net-tools)",
    },
}

def pick_tool() -> str:
    if TOOLS["ss"]["exists"]:
        return "ss"
    if TOOLS["netstat"]["exists"]:
        return "netstat"
    return ""

def run_shell(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)

# ------------------------ Core Lab Functions -------------------------

def list_active_connections() -> str:
    tool = pick_tool()
    if not tool:
        return (
            "ERROR: Neither 'ss' nor 'netstat' found.\n"
            "Install netstat with: sudo apt update && sudo apt install -y net-tools\n"
        )
    cmd = TOOLS[tool]["cmd_all"]
    result = run_shell(cmd)
    if result.returncode != 0:
        return f"ERROR running '{cmd}':\n{result.stderr}"
    header = (f"Tool: {TOOLS[tool]['pretty']}\n"
              f"Command: {cmd}\n"
              f"Timestamp: {datetime.now().isoformat()}\n")
    return header + "\n" + result.stdout

def filter_mysql_connections(raw: str, ports=(3306, 33060)) -> str:
    """Filter connections that look like MySQL by port or process name."""
    lines = raw.splitlines()
    data_lines = lines[:]

    port_patterns = [re.compile(rf":{p}(\b|\s|$)") for p in ports]
    name_patterns = [re.compile(r"mysqld?", re.IGNORECASE)]

    filtered = []
    for ln in data_lines:
        if any(p.search(ln) for p in port_patterns) or any(n.search(ln) for n in name_patterns):
            filtered.append(ln)

    if not filtered:
        return (
            "No MySQL-like connections found by port/name heuristics.\n"
            "Tip: Ensure the MySQL container is running and actively connected.\n"
        )

    # Extract PIDs (users:(("mysqld",pid=1234,...)) or PID/Program)
    pid_candidates = set()
    pid_regexes = [
        re.compile(r"pid=(\d+)", re.IGNORECASE),
        re.compile(r"\b(\d+)/(mysqld?)\b", re.IGNORECASE),
        re.compile(r"\b(\d+)/(docker-proxy)\b", re.IGNORECASE),
    ]
    for ln in filtered:
        for rgx in pid_regexes:
            for m in rgx.finditer(ln):
                try:
                    pid_candidates.add(int(m.group(1)))
                except Exception:
                    pass

    out = [
        "Filtered view: likely MySQL connections (by port/name heuristics)",
        "------------------------------------------------------------------",
        *filtered,
    ]
    if pid_candidates:
        out.append("\nPotential PID(s) involved (heuristic): " + ", ".join(map(str, sorted(pid_candidates))))
        out.append("If you intend to terminate a malicious connection, confirm the correct PID first!")
    else:
        out.append(
            "\nNo PID could be parsed from lines.\n"
            "Check the full active list (Menu 1) to identify PID, or use 'ps aux | grep mysql'.")
    return "\n".join(out)

def mysql_hunt_deep() -> str:
    """Broader hunt: LISTEN sockets, ACTIVE, and UNIX sockets; includes sudo hints."""
    tool = pick_tool()
    if not tool:
        return (
            "ERROR: Neither 'ss' nor 'netstat' found.\n"
            "Install with: sudo apt update && sudo apt install -y net-tools\n"
        )
    sections = []
    if tool == "ss":
        cmds = [
            ("LISTEN TCP (3306/33060)",
             "ss -ltnp | grep -E '(:3306\\b|:33060\\b|mysqld)' || true"),
            ("ACTIVE TCP/UDP",
             "ss -tunap | grep -E '(:3306\\b|:33060\\b|mysqld)' || true"),
            ("UNIX sockets",
             "ss -xap | grep -i mysql || true"),
        ]
    else:
        cmds = [
            ("LISTEN TCP (3306/33060)",
             "netstat -ltnp | grep -E '(:3306\\b|:33060\\b|mysqld)' || true"),
            ("ACTIVE TCP/UDP",
             "netstat -tunap | grep -E '(:3306\\b|:33060\\b|mysqld)' || true"),
            ("UNIX sockets",
             "netstat -xap | grep -i mysql || true"),
        ]
    for title, cmd in cmds:
        r = run_shell(cmd)
        body = r.stdout.strip() or "(no matches)"
        sections.append(f"## {title}\n$ {cmd}\n{body}\n")
    return ("\n".join(sections) +
            "\nIf everything says '(no matches)':\n"
            "• MySQL may be UNIX-socket only (no TCP listener).\n"
            "• You may still need sudo to see PIDs: sudo -E python3 netstat_lab_helper.py\n"
            "• Ensure container maps/binds TCP 3306/33060. Open a TCP client to create an active entry.\n")

# ----------------------- Reflection Template ------------------------
REFLECTION_TEMPLATE = f"""
Network Monitoring Reflection (Task 4)
============================================================
Name: ______________________________   Date: {datetime.now().date()}
Course/Section: ______________________

1) Why is it important to monitor active connections on a server, especially
   during a potential attack? (Use your observations from Task 2.)
   \nAnswer:\n- 
- 
- 

2) In your lab, which MySQL-related connection(s) did you observe? Include
   details such as local/remote addresses, state, and PID.
   \nAnswer:\n- 
- 

3) If you terminated a (simulated) malicious connection (Task 3), what was the
   PID and what evidence led you to conclude it was malicious/suspicious?
   \nAnswer:\n- 
- 

4) Discuss the significance of identifying and terminating malicious connections
   in cybersecurity operations. What are the risks of terminating the wrong PID,
   and how can defenders minimize disruption while responding quickly?
   \nAnswer:\n- 
- 

5) Based on this exercise, list **two** best practices for ongoing network
   monitoring and incident response on production systems.
   \nAnswer:\n- 
- 

(Attach screenshots or saved snapshots from lab_outputs/ as evidence.)
"""

def save_snapshot(text: str, prefix: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = OUT_DIR / f"{prefix}_{ts}.txt"
    path.write_text(text, encoding="utf-8")
    return path

def generate_reflection_file() -> Path:
    path = OUT_DIR / "Task4_Reflection_Template.txt"
    path.write_text(REFLECTION_TEMPLATE, encoding="utf-8")
    return path

# ----------------------------- Menu UI ------------------------------
MENU = """
============================================================
 Network Statistics Helper — Task 2 to Task 4
============================================================
1) Show ALL active TCP/UDP connections with PIDs (netstat/ss)
2) Show LIKELY MySQL connections (port/name heuristics + deep hunt)
3) Save FULL active connections snapshot to file
4) Save MySQL-filtered snapshot to file
5) Terminate a PID (kill) — USE WITH CAUTION
6) Generate the Task 4 Reflection template file
7) About / Quick Tips
0) Exit
"""

ABOUT = f"""
ABOUT / QUICK TIPS
------------------------------------------------------------
• This helper prefers 'ss -tunap' if available; otherwise 'netstat -tunap'.
• If neither is found, install netstat with:
    sudo apt update && sudo apt install -y net-tools
• If PIDs/program names are missing, run with:
    sudo -E python3 netstat_lab_helper.py
• MySQL default ports: 3306; some installs also expose 33060 (X Protocol).
• MySQL may use only a UNIX socket (no TCP). Use the deep hunt (Option 2).
• After killing, re-run option 1 or 2 to verify the connection is gone.
• Saved outputs go to: {OUT_DIR}
• Reflection template (Task 4) helps you craft a strong write-up.
"""

def main():
    while True:
        try:
            clear_screen()
            print(MENU)
            choice = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if choice == "1":
            clear_screen()
            txt = list_active_connections()
            print(txt)
            pause()
        elif choice == "2":
            clear_screen()
            base = list_active_connections()
            if base.startswith("ERROR"):
                print(base)
            else:
                ports = MYSQL_DEFAULT_PORTS["mysql"]
                if not isinstance(ports, (list, tuple)):
                    ports = (ports,)
                filt = filter_mysql_connections(base, ports=ports)
                print(filt)
                # Always offer deeper checks so students see useful output
                print("\n--- Deep Hunt (LISTEN + UNIX sockets) ---\n")
                print(mysql_hunt_deep())
            pause()
        elif choice == "3":
            clear_screen()
            base = list_active_connections()
            if base.startswith("ERROR"):
                print(base)
            else:
                p = save_snapshot(base, prefix="active_connections_full")
                print(f"Saved full snapshot to: {p}")
            pause()
        elif choice == "4":
            clear_screen()
            base = list_active_connections()
            if base.startswith("ERROR"):
                print(base)
            else:
                ports = MYSQL_DEFAULT_PORTS["mysql"]
                if not isinstance(ports, (list, tuple)):
                    ports = (ports,)
                filt = filter_mysql_connections(base, ports=ports)
                p = save_snapshot(filt, prefix="active_connections_mysql")
                print(f"Saved MySQL-filtered snapshot to: {p}")
            pause()
        elif choice == "5":
            clear_screen()
            print("Terminate a PID (Use with caution)\n" + "-" * 40)
            print("Tip: Use Menu 1 or 2 to see candidate PIDs first.\n")
            pid_str = input("Enter the PID to terminate (or 'q' to cancel): ").strip()
            if pid_str.lower() == 'q':
                print("Cancelled."); pause(); continue
            if not pid_str.isdigit():
                print("Invalid PID. Must be a positive integer."); pause(); continue
            pid = int(pid_str)
            # Show process preview
            ps_out = run_shell(f"ps -p {pid} -o pid,comm,cmd --no-headers").stdout.strip()
            if ps_out:
                print("\nProcess preview:\n" + ps_out + "\n")
            else:
                print("\nWarning: Could not preview process details (PID may not exist).\n")
            confirm = input("Type 'YES' to send SIGTERM to this PID: ").strip()
            if confirm != 'YES':
                print("Not confirmed. No action taken."); pause(); continue
            res = run_shell(f"kill {pid}")
            if res.returncode == 0:
                print(f"\nSIGTERM sent to PID {pid}. Check connections again (Menu 1/2).")
            else:
                print(f"\nSIGTERM failed: {res.stderr.strip()}")
                hard = input("Send SIGKILL (9)? Type 'KILL' to proceed: ").strip()
                if hard == 'KILL':
                    res2 = run_shell(f"kill -9 {pid}")
                    if res2.returncode == 0:
                        print(f"SIGKILL sent to PID {pid}. Verify with Menu 1/2.")
                    else:
                        print(f"SIGKILL failed: {res2.stderr.strip()}\n"
                              "PID may not exist or you may need elevated permissions.")
                else:
                    print("No further action taken.")
            pause()
        elif choice == "6":
            clear_screen()
            p = OUT_DIR / "Task4_Reflection_Template.txt"
            p.write_text(REFLECTION_TEMPLATE, encoding="utf-8")
            print(f"Reflection template created: {p}\n\nOpen it, fill it in, and include in your report.")
            pause()
        elif choice == "7":
            clear_screen()
            print(ABOUT)
            pause()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
            pause()

if __name__ == "__main__":
    main()
