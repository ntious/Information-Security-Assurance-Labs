#!/usr/bin/env python3
import os, sys, platform, shutil, subprocess, datetime, re

BANNER = r"""
====================================================
            N M A P   T E A C H I N G   T O O L
====================================================
Use responsibly. Scan only hosts you have permission to scan.
"""

def is_root_like():
    if os.name == "nt":
        # Windows doesn't have EUID; require admin for raw scans anyway
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0

def nmap_path():
    return shutil.which("nmap")

def prompt_yes_no(msg, default="y"):
    ans = input(f"{msg} [{'Y/n' if default.lower()=='y' else 'y/N'}]: ").strip().lower()
    if ans == "" and default:
        ans = default
    return ans.startswith("y")

def run_cmd(cmd, shell=False):
    try:
        proc = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        return 1, "", str(e)

def suggest_install_commands():
    system = platform.system().lower()
    cmds = []
    if "linux" in system:
        # try to detect package manager
        if shutil.which("apt") or shutil.which("apt-get"):
            cmds = ["sudo apt update", "sudo apt install -y nmap"]
        elif shutil.which("dnf"):
            cmds = ["sudo dnf install -y nmap"]
        elif shutil.which("yum"):
            cmds = ["sudo yum install -y nmap"]
        elif shutil.which("pacman"):
            cmds = ["sudo pacman -S --noconfirm nmap"]
    elif "darwin" in system:  # macOS
        if shutil.which("brew"):
            cmds = ["brew update", "brew install nmap"]
        else:
            cmds = ["# Install Homebrew first:", '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                    "brew install nmap"]
    elif "windows" in system:
        if shutil.which("choco"):
            cmds = ["choco install nmap -y"]
        elif shutil.which("winget"):
            cmds = ["winget install -e --id Insecure.Nmap"]
        else:
            cmds = ["# Download installer:", "https://nmap.org/download.html", "# Then run the installer for Windows."]
    return cmds

def try_install_nmap():
    cmds = suggest_install_commands()
    if not cmds:
        print("\nCould not determine a package manager. Please install Nmap from https://nmap.org/download.html")
        return False
    print("\nInstallation steps I can run or that you can copy/paste:")
    for c in cmds:
        print("  ", c)
    if any(c.startswith("#") or c.startswith("http") for c in cmds):
        # Can't auto-run comments/links
        return prompt_yes_no("\nOpen installer instructions in your browser? (not automated)", default="n")
    if prompt_yes_no("\nAttempt to run these commands automatically now?", default="n"):
        all_ok = True
        for c in cmds:
            code, out, err = run_cmd(c, shell=True)
            if out.strip():
                print(out)
            if err.strip():
                print(err, file=sys.stderr)
            if code != 0:
                all_ok = False
                break
        return all_ok
    return False

def valid_target(s):
    # Simple sanity check for IPv4, IPv6, or hostname
    ipv4 = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    ipv6 = re.compile(r"^[0-9a-fA-F:]+$")
    hostname = re.compile(r"^[A-Za-z0-9\-\.]+$")
    return bool(ipv4.match(s) or ipv6.match(s) or hostname.match(s))

def menu():
    print("""
Choose a scan profile:
  1) Quick TCP (top 1000)            [-sT/-sS -T3]
  2) Default scripts + versions      [-sC -sV -T4]
  3) Full TCP (all 65535 ports)      [-p- -T4]
  4) Service/version only            [-sV -T4]
  5) OS detection (root/admin best)  [-O -T4]
  6) Aggressive (OS+scripts+vers)    [-A -T4]
  7) UDP top 100 (slow)              [-sU --top-ports 100 -T4]
  8) Custom flags (advanced)
""")

def build_command(choice, target, syn_ok):
    base = ["nmap"]
    tcp_scan = ["-sS" if syn_ok else "-sT"]
    if choice == "1":
        return base + tcp_scan + ["-T3", target]
    elif choice == "2":
        return base + ["-sC", "-sV", "-T4"] + tcp_scan + [target]
    elif choice == "3":
        return base + tcp_scan + ["-p-", "-T4", target]
    elif choice == "4":
        return base + ["-sV", "-T4"] + tcp_scan + [target]
    elif choice == "5":
        # OS detection benefits from root; include tcp_scan too
        return base + tcp_scan + ["-O", "-T4", target]
    elif choice == "6":
        # -A implies -O -sV -sC and more
        return base + ["-A", "-T4"] + tcp_scan + [target]
    elif choice == "7":
        return base + ["-sU", "--top-ports", "100", "-T4", target]
    elif choice == "8":
        flags = input("Enter your custom Nmap flags (e.g., -sV -p 1-1024 -T4): ").strip().split()
        return base + flags + [target]
    else:
        return None

def save_output(text, default_prefix="nmap_scan"):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"{default_prefix}_{ts}.txt"
    fname = input(f"Save as [{default_name}]: ").strip()
    if not fname:
        fname = default_name
    with open(fname, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\nSaved: {os.path.abspath(fname)}")

def main():
    print(BANNER)
    # 1) Check nmap availability
    if not nmap_path():
        print("Nmap is not installed or not in PATH.")
        if try_install_nmap():
            # Re-check
            if not nmap_path():
                print("\nNmap still not found in PATH. Please restart the terminal or ensure PATH is updated.")
                sys.exit(1)
        else:
            print("\nPlease install Nmap and re-run this tool.")
            sys.exit(1)

    # 2) Target
    target = input("Enter target IP/hostname (single target): ").strip()
    if not valid_target(target):
        print("Invalid target. Use a valid IP or hostname.")
        sys.exit(1)

    # 3) Menu
    syn_ok = is_root_like()
    if not syn_ok:
        print("\nNote: Not running as root/admin; using TCP connect scans (-sT) instead of SYN scans (-sS).")
    menu()
    choice = input("Select option [1-8]: ").strip()
    cmd = build_command(choice, target, syn_ok)
    if not cmd:
        print("Invalid selection.")
        sys.exit(1)

    print("\nRunning:", " ".join(cmd))
    print("----------------------------------------------------\n")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        print(out)
        if prompt_yes_no("\nSave output to a text file?", default="y"):
            save_output(out)
    except KeyboardInterrupt:
        print("\nScan cancelled.")
    except Exception as e:
        print(f"\nError running scan: {e}")

if __name__ == "__main__":
    main()
