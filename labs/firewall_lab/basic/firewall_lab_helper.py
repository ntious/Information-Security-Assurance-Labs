#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
firewall_lab_helper.py
====================================================
A freshman-friendly, menu-driven Python helper to complete
"Implementing Technical Security Controls – Part 1 (UFW Firewall on Ubuntu)".

⚠️ ETHICS & PERMISSION
----------------------------------------------------
Only modify firewalls on systems you own or have *explicit written permission* to manage.
If you're in a university sandbox/VM, follow your instructor's rules and restore defaults if required.

WHAT THIS SCRIPT DOES
----------------------------------------------------
- Detects IP address (Ubuntu).
- Checks UFW status and guides you to enable it.
- Adds/removes allow/deny rules for common ports (HTTP 80, HTTPS 443, SSH 22).
- Sets default policies (e.g., default deny incoming).
- Allows/blocks specific IP addresses (e.g., allow SSH from a trusted IP).
- Verifies rules and shows numbered rules.
- Optional "dry run" mode (prints commands instead of executing) for environments without sudo (e.g., some Codespaces).
- Optional "advanced" menu: logging, rate-limit SSH, export/restore rules, reset UFW.

REQUIREMENTS
----------------------------------------------------
- Ubuntu-based system with 'ufw' installed.
- Python 3.8+
- For real changes, you need to run with sudo OR have permission to run 'sudo ufw ...' commands.
- For verification tests: 'curl' (HTTP/HTTPS) and 'telnet' or 'nc' (optional for blocked-port test).

USAGE
----------------------------------------------------
python3 firewall_lab_helper.py
(You will be presented with a menu.)

Author: Your Teaching Team
"""
from __future__ import annotations
import os
import sys
import shlex
import subprocess
from typing import List, Tuple

# ----------- Utilities -----------

def run(cmd: str, dry_run: bool=False) -> Tuple[int, str, str]:
    """
    Run a shell command safely.
    Returns: (returncode, stdout, stderr).
    If dry_run=True, prints the command and returns (0, "", "").
    """
    print(f"\n$ {cmd}")
    if dry_run:
        print("[dry-run] Command not executed.")
        return 0, "", ""
    try:
        p = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=False)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd}"
    except Exception as e:
        return 1, "", str(e)


def require_ubuntu_hint():
    print("\n[Hint] This lab is designed for Ubuntu. If you are on Windows/macOS, run it inside your course Ubuntu VM or WSL.\n")


def detect_ip() -> str:
    """Try multiple ways to get the primary IP address on Ubuntu."""
    candidates = [
        "hostname -I",
        "ip -4 addr show scope global | awk '/inet /{print $2}' | cut -d/ -f1 | head -n1",
        "ifconfig | awk '/inet / && $2 != \"127.0.0.1\" {print $2; exit}'"
    ]
    for c in candidates:
        code, out, err = run(c)
        if code == 0 and out:
            # Take first token if needed
            return out.split()[0]
    return "Unknown"


def ufw_present() -> bool:
    code, _, _ = run("which ufw")
    return code == 0


def ufw_status() -> str:
    code, out, err = run("sudo ufw status verbose")
    if code != 0:
        # Try without sudo (some sandboxes alias or allow ufw without sudo)
        code2, out2, err2 = run("ufw status verbose")
        if code2 == 0:
            return out2 or "(No output)"
        return f"(Could not read status) {err or err2}"
    return out or "(No output)"


def ensure_enabled(dry: bool):
    print("\n[Step] Enable the firewall if inactive.")
    code, out, err = run("sudo ufw status", dry)
    text = out.lower()
    if "inactive" in text:
        print("\n[Action] UFW is inactive. Enabling...")
        run("sudo ufw enable", dry)
    else:
        print("\n[Info] UFW already active (or status unavailable).")
    print("\nCurrent status:")
    print(ufw_status())


def allow_common_ports(dry: bool):
    print("\n[Step] Allow HTTP (80/tcp), HTTPS (443/tcp), and SSH (22/tcp).")
    run("sudo ufw allow 80/tcp", dry)
    run("sudo ufw allow 443/tcp", dry)
    run("sudo ufw allow 22/tcp", dry)
    print("\nCurrent status:")
    print(ufw_status())


def set_default_deny_incoming(dry: bool):
    print("\n[Step] Set default policy: deny all incoming.")
    run("sudo ufw default deny incoming", dry)
    print("\nCurrent status:")
    print(ufw_status())


def block_specific_ports(dry: bool):
    print("\n[Step] Block specific legacy/unsafe ports (examples: FTP 21, Telnet 23).")
    run("sudo ufw deny 21/tcp", dry)
    run("sudo ufw deny 23/tcp", dry)
    print("\nCurrent status:")
    print(ufw_status())


def allow_ssh_from_ip(ip: str, dry: bool):
    print(f"\n[Step] Allow SSH (22/tcp) from trusted IP {ip}.")
    run(f"sudo ufw allow from {ip} to any port 22", dry)
    print("\nCurrent status:")
    print(ufw_status())


def deny_all_from_ip(ip: str, dry: bool):
    print(f"\n[Step] Deny all traffic from IP {ip}.")
    run(f"sudo ufw deny from {ip}", dry)
    print("\nCurrent status:")
    print(ufw_status())


def show_numbered_rules():
    print("\n[Step] Show numbered rules (useful for deletes).")
    print(ufw_status())


def delete_rule_by_number(n: str, dry: bool):
    print(f"\n[Step] Delete UFW rule number {n}.")
    run(f"sudo ufw delete {n}", dry)
    print("\nCurrent status:")
    print(ufw_status())


def test_http_https(ip: str, dry: bool):
    print("\n[Verify] Test HTTP/HTTPS with curl (server must be running).")
    if ip == "Unknown":
        ip = input("Enter your server IP/domain (e.g., 127.0.0.1 or example.com): ").strip()
    run(f"curl -I http://{ip}", dry)
    run(f"curl -I https://{ip}", dry)


def test_blocked_port(ip: str, port: str="21", dry: bool=False):
    print("\n[Verify] Test a blocked port (FTP 21/tcp by default).")
    if ip == "Unknown":
        ip = input("Enter your server IP/domain: ").strip()
    # Try telnet, then nc
    code, _, _ = run(f"telnet {ip} {port}", dry)
    if code != 0:
        print("[Info] 'telnet' not available or blocked; trying 'nc' (netcat)...")
        run(f"nc -vz {ip} {port}", dry)


# ----------- Advanced helpers -----------

def toggle_logging(level: str, dry: bool):
    """
    UFW logging levels: off, low, medium, high, full
    """
    print(f"\n[Advanced] Set UFW logging level to '{level}'.")
    run(f"sudo ufw logging {level}", dry)
    print("\nCurrent status:")
    print(ufw_status())


def rate_limit_ssh(dry: bool):
    """
    Rate-limit SSH to mitigate brute-force attempts.
    """
    print("\n[Advanced] Enable SSH rate limiting (mitigates brute-force).")
    run("sudo ufw limit 22/tcp", dry)
    print("\nCurrent status:")
    print(ufw_status())


def export_rules(filepath: str, dry: bool):
    """
    Export UFW rules for backup (reads from /etc/ufw/user.rules if accessible).
    Non-root users may need sudo tee to write.
    """
    print(f"\n[Advanced] Export UFW rules to {filepath}.")
    # Read using sudo cat; write with Python
    code, out, err = run("sudo cat /etc/ufw/user.rules")
    if code == 0 and out:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(out + "\n")
            print(f"[OK] Exported to {filepath}")
        except Exception as e:
            print(f"[Error] Could not write to {filepath}: {e}")
    else:
        print("[Warn] Could not read /etc/ufw/user.rules (need permission). Try running this script with sudo.")


def restore_rules(filepath: str, dry: bool):
    """
    Restore UFW rules from a local file (overwrites user.rules).
    """
    print(f"\n[Advanced] Restore UFW rules from {filepath}.")
    if not os.path.exists(filepath):
        print("[Error] File does not exist.")
        return
    if dry:
        print("[dry-run] Would copy rules to /etc/ufw/user.rules and reload ufw.")
        return
    # Copy via sudo tee
    code, _, err = run(f"sudo sh -c 'cat {shlex.quote(filepath)} > /etc/ufw/user.rules'")
    if code == 0:
        print("[OK] Rules restored. Reloading UFW...")
        run("sudo ufw reload")
    else:
        print(f"[Error] Could not restore rules: {err}")


def ufw_reset(dry: bool):
    print("\n[Advanced] Reset UFW to defaults (⚠️ removes all rules).")
    run("sudo ufw --force reset", dry)
    print("\nCurrent status:")
    print(ufw_status())


# ----------- Menus -----------

def intro():
    print(r"""
====================================================
UFW FIREWALL LAB HELPER (Freshman-Friendly)
====================================================
This tool guides you through:
  1) Finding your IP
  2) Checking/Enabling UFW
  3) Allowing/Blocking key ports (80/443/22, 21/23)
  4) Allowing/Blocking specific IPs
  5) Verifying with curl/telnet
  6) (Advanced) Logging, SSH rate-limit, export/restore, reset

Tip: If you don't have sudo access (e.g., some Codespaces),
use DRY-RUN mode to print commands you can copy into a terminal.

""")
    require_ubuntu_hint()


def main():
    intro()
    dry_run = False
    ip = detect_ip()
    print(f"[Info] Detected IP: {ip}")

    while True:
        print(r"""
---------------- MENU ----------------
[1]  Show UFW status (verbose)
[2]  Enable UFW (if inactive)
[3]  Allow common ports: 80, 443, 22
[4]  Set default deny incoming
[5]  Block specific ports: 21 (FTP), 23 (Telnet)
[6]  Allow SSH (22) from a specific IP
[7]  Deny all traffic from a specific IP
[8]  Show numbered rules
[9]  Delete a rule by number
[10] Verify HTTP/HTTPS with curl
[11] Test a blocked port (default 21)
[12] Toggle DRY-RUN mode (currently: {dry})
----- Advanced (optional) -----
[13] Set logging level (off/low/medium/high/full)
[14] Rate-limit SSH (mitigate brute force)
[15] Export rules to file
[16] Restore rules from file
[17] Reset UFW to defaults (⚠️ removes rules)
[q]  Quit
--------------------------------------
""".format(dry="ON" if dry_run else "OFF"))

        choice = input("Pick an option: ").strip().lower()
        if choice == "1":
            print("\nCurrent status:")
            print(ufw_status())
        elif choice == "2":
            ensure_enabled(dry_run)
        elif choice == "3":
            allow_common_ports(dry_run)
        elif choice == "4":
            set_default_deny_incoming(dry_run)
        elif choice == "5":
            block_specific_ports(dry_run)
        elif choice == "6":
            tip = input("Enter trusted IP for SSH (e.g., 192.168.1.100): ").strip()
            allow_ssh_from_ip(tip, dry_run)
        elif choice == "7":
            bip = input("Enter IP to block entirely (e.g., 203.0.113.1): ").strip()
            deny_all_from_ip(bip, dry_run)
        elif choice == "8":
            show_numbered_rules()
        elif choice == "9":
            n = input("Enter rule number to delete (see [8]): ").strip()
            delete_rule_by_number(n, dry_run)
        elif choice == "10":
            test_http_https(ip, dry_run)
        elif choice == "11":
            p = input("Enter blocked port to test (default 21): ").strip() or "21"
            test_blocked_port(ip, p, dry_run)
        elif choice == "12":
            dry_run = not dry_run
            print(f"[Info] DRY-RUN is now {'ON' if dry_run else 'OFF'}.")
        elif choice == "13":
            lvl = input("Logging level (off/low/medium/high/full): ").strip().lower()
            if lvl in {"off","low","medium","high","full"}:
                toggle_logging(lvl, dry_run)
            else:
                print("[Error] Invalid level.")
        elif choice == "14":
            rate_limit_ssh(dry_run)
        elif choice == "15":
            path = input("Export to file path (e.g., ufw_rules.backup): ").strip() or "ufw_rules.backup"
            export_rules(path, dry_run)
        elif choice == "16":
            path = input("Restore from file path: ").strip()
            restore_rules(path, dry_run)
        elif choice == "17":
            confirm = input("Type 'RESET' to confirm resetting UFW to defaults: ").strip()
            if confirm == "RESET":
                ufw_reset(dry_run)
            else:
                print("[Info] Reset cancelled.")
        elif choice in {"q", "quit", "exit"}:
            print("Goodbye!")
            break
        else:
            print("Please choose a valid option.")

if __name__ == "__main__":
    main()
