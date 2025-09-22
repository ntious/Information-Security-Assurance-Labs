#!/usr/bin/env python3
"""
student_recon_tool.py
====================================================
A freshman-friendly, menu-driven Python tool that helps students analyze basic
security threats and vulnerabilities through **network reconnaissance** tasks,
inspired by your course handout.

⚠️ **ETHICS & PERMISSION**
----------------------------------------------------------------
Only scan systems you own or have *explicit written permission* to test.
Unauthorized scanning can be illegal and against university policy.

This script:
- Asks for a target (domain or IP)
- Offers a simple menu of recon tasks (ping, DNS, WHOIS, traceroute, Nmap scans)
- Saves outputs into a timestamped folder
- Summarizes Nmap results (open ports, services, basic risk hints)
- Is cross‑platform aware (Windows/macOS/Linux), and checks for required tools

Note: Some tasks require external tools to be installed:
- `nmap`     : https://nmap.org/download.html
- `whois`    : Often preinstalled on Linux/macOS (brew install whois). On Windows, consider WSL or third‑party whois.
- `traceroute` / `tracert` : Built‑in on most systems (Windows uses `tracert`).

Author: Your Teaching Team
License: MIT
"""
from __future__ import annotations
import os
import re
import sys
import shlex
import json
import time
import shutil
import socket
import platform
import datetime
import subprocess
import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple, Dict

# -------------------------------
# Utility helpers
# -------------------------------

def banner(title: str) -> None:
    print("\n" + "="*70)
    print(title)
    print("="*70 + "\n")

def pause() -> None:
    input("\nPress ENTER to continue...")

def which(cmd: str) -> Optional[str]:
    """Return full path to an executable or None if not found."""
    return shutil.which(cmd)

def run_cmd(cmd: List[str], outfile: Optional[str] = None) -> Tuple[int, str, str]:
    """Run a command safely, capture output, and optionally write to a file."""
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = proc.communicate()
        code = proc.returncode
    except FileNotFoundError as e:
        return (127, "", f"Command not found: {cmd[0]}")
    except Exception as e:
        return (1, "", f"Failed to run {' '.join(cmd)}: {e}")
    if outfile:
        try:
            with open(outfile, "w", encoding="utf-8", errors="ignore") as f:
                f.write(out)
                if err:
                    f.write("\n--- STDERR ---\n")
                    f.write(err)
        except Exception as e:
            print(f"[!] Could not write to {outfile}: {e}")
    return (code, out, err)

def ensure_tools(tools: List[str]) -> Dict[str, bool]:
    """Check for required command-line tools; return availability map."""
    available = {}
    for t in tools:
        available[t] = which(t) is not None
    return available

def resolve_target(target: str) -> List[str]:
    """Resolve a domain to IP(s). If already an IP, return it as list."""
    try:
        socket.inet_aton(target)
        return [target]
    except OSError:
        pass
    try:
        infos = socket.getaddrinfo(target, None)
        ips = sorted({item[4][0] for item in infos if item[4]})
        return ips
    except Exception:
        return []

# -------------------------------
# Report & folder management
# -------------------------------

def new_output_dir(base: str = "recon_results") -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(os.getcwd(), f"{base}_{ts}")
    os.makedirs(folder, exist_ok=True)
    return folder

def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# -------------------------------
# Summarization (Nmap XML parsing)
# -------------------------------

def parse_nmap_xml(xml_path: str) -> Dict:
    """
    Parse minimal Nmap XML and extract:
      - host status
      - open ports (port, protocol, service name, product/version if present)
    """
    data = {"hosts": []}
    if not os.path.exists(xml_path):
        return data
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for host in root.findall("host"):
            host_data = {"address": None, "status": None, "ports": []}
            addr = host.find("address")
            if addr is not None and addr.attrib.get("addr"):
                host_data["address"] = addr.attrib.get("addr")
            status = host.find("status")
            if status is not None and status.attrib.get("state"):
                host_data["status"] = status.attrib.get("state")
            ports = host.find("ports")
            if ports is not None:
                for p in ports.findall("port"):
                    proto = p.attrib.get("protocol")
                    portid = p.attrib.get("portid")
                    state_el = p.find("state")
                    state = state_el.attrib.get("state") if state_el is not None else None
                    service_el = p.find("service")
                    svc_name = service_el.attrib.get("name") if service_el is not None else None
                    product = service_el.attrib.get("product") if service_el is not None else None
                    version = service_el.attrib.get("version") if service_el is not None else None
                    host_data["ports"].append({
                        "protocol": proto,
                        "port": portid,
                        "state": state,
                        "service": svc_name,
                        "product": product,
                        "version": version
                    })
            data["hosts"].append(host_data)
    except Exception as e:
        data["error"] = str(e)
    return data

def basic_risk_hints(port: int, service: str | None) -> List[str]:
    """Very lightweight, educational hints. *Not* a vulnerability scan."""
    hints = []
    if service:
        s = service.lower()
    else:
        s = ""
    if port in (20, 21) or "ftp" in s:
        hints.append("FTP often allows cleartext creds; prefer SFTP/FTPS.")
    if port in (22,) or "ssh" in s:
        hints.append("Ensure strong passwords/keys, disable root login, limit users.")
    if port in (23,) or "telnet" in s:
        hints.append("Telnet is insecure (cleartext). Disable; use SSH instead.")
    if port in (25, 465, 587) or "smtp" in s:
        hints.append("Check for open relay; enforce TLS.")
    if port in (80, 8080) or "http" in s:
        hints.append("Use HTTPS (TLS); check for default pages or outdated apps.")
    if port in (443,) or "https" in s or "ssl" in s or "tls" in s:
        hints.append("Ensure modern TLS; disable weak ciphers/SSLv2/3.")
    if port in (3306,) or "mysql" in s:
        hints.append("Restrict DB access to internal network; strong creds.")
    if port in (3389,) or "ms-wbt-server" in s or "rdp" in s:
        hints.append("Protect RDP with MFA, lockout policy, and updates.")
    if port in (5900,) or "vnc" in s:
        hints.append("VNC often weak; require strong auth and tunnel over SSH/VPN.")
    return hints

def summarize_nmap(xml_path: str, md_out: str) -> str:
    parsed = parse_nmap_xml(xml_path)
    lines = ["# Nmap Summary (Educational)"]
    if "error" in parsed:
        lines.append(f"Parser error: {parsed['error']}")
    for host in parsed.get("hosts", []):
        lines.append(f"## Host: {host.get('address')} (status: {host.get('status')})")
        if not host.get("ports"):
            lines.append("- No ports found/open in parsed data.")
            continue
        for p in host["ports"]:
            if p.get("state") != "open":
                continue
            port = int(p.get("port")) if p.get("port") else -1
            service = p.get("service") or "unknown"
            product = p.get("product") or ""
            version = p.get("version") or ""
            svc_line = f"- {p.get('protocol')}/{p.get('port')} open — service: {service}"
            if product or version:
                svc_line += f" ({product} {version})"
            lines.append(svc_line)
            # Add simple hints
            for hint in basic_risk_hints(port, service):
                lines.append(f"  - Hint: {hint}")
    content = "\n".join(lines) + "\n"
    write_text(md_out, content)
    return content

# -------------------------------
# Recon tasks
# -------------------------------

def task_ping(target: str, outdir: str) -> None:
    banner("[PING] Basic Connectivity Test")
    count_flag = "-c" if platform.system().lower() != "windows" else "-n"
    cmd = ["ping", count_flag, "4", target]
    code, out, err = run_cmd(cmd, os.path.join(outdir, "ping.txt"))
    print(out or err or f"Exit code: {code}")

def task_dns_lookup(target: str, outdir: str) -> None:
    banner("[DNS] Name Resolution")
    # Prefer 'nslookup' (common across OS); fall back to 'dig' if available
    if which("nslookup"):
        cmd = ["nslookup", target]
        code, out, err = run_cmd(cmd, os.path.join(outdir, "dns_nslookup.txt"))
        print(out or err or f"Exit code: {code}")
    elif which("dig"):
        cmd = ["dig", target, "ANY", "+short"]
        code, out, err = run_cmd(cmd, os.path.join(outdir, "dns_dig.txt"))
        print(out or err or f"Exit code: {code}")
    else:
        print("[!] Neither nslookup nor dig is available. Skipping DNS lookup.")

def task_whois(target: str, outdir: str) -> None:
    banner("[WHOIS] Domain Registration Info")
    if which("whois"):
        cmd = ["whois", target]
        code, out, err = run_cmd(cmd, os.path.join(outdir, "whois.txt"))
        print(out or err or f"Exit code: {code}")
    else:
        print("[!] 'whois' command is not installed. Consider installing it to use this feature.")

def task_traceroute(target: str, outdir: str) -> None:
    banner("[TRACEROUTE] Network Path")
    tracer = "tracert" if platform.system().lower() == "windows" else "traceroute"
    if which(tracer):
        cmd = [tracer, target]
        code, out, err = run_cmd(cmd, os.path.join(outdir, f"{tracer}.txt"))
        print(out or err or f"Exit code: {code}")
    else:
        print(f"[!] '{tracer}' is not available on this system.")

def ensure_nmap_or_warn() -> bool:
    if which("nmap"):
        return True
    print("[!] 'nmap' is not installed or not on PATH.")
    print("    Please install Nmap: https://nmap.org/download.html")
    return False

def task_nmap_quick_scan(target: str, outdir: str) -> None:
    banner("[NMAP] Quick Scan (Top Ports, Faster Timing)")
    if not ensure_nmap_or_warn():
        return
    xml = os.path.join(outdir, "nmap_quick.xml")
    cmd = ["nmap", "-T4", "-F", "-oX", xml, target]
    code, out, err = run_cmd(cmd, os.path.join(outdir, "nmap_quick.txt"))
    print(out or err or f"Exit code: {code}")
    print("\n[Summary]\n" + summarize_nmap(xml, os.path.join(outdir, "SUMMARY_nmap_quick.md")))

def task_nmap_service_version(target: str, outdir: str) -> None:
    banner("[NMAP] SYN + Service Version Detection")
    if not ensure_nmap_or_warn():
        return
    xml = os.path.join(outdir, "nmap_service_version.xml")
    cmd = ["nmap", "-sS", "-sV", "-T4", "-oX", xml, target]
    code, out, err = run_cmd(cmd, os.path.join(outdir, "nmap_service_version.txt"))
    print(out or err or f"Exit code: {code}")
    print("\n[Summary]\n" + summarize_nmap(xml, os.path.join(outdir, "SUMMARY_nmap_service_version.md")))

def task_nmap_os_detect(target: str, outdir: str) -> None:
    banner("[NMAP] OS Detection")
    if not ensure_nmap_or_warn():
        return
    xml = os.path.join(outdir, "nmap_os_detect.xml")
    cmd = ["nmap", "-O", "-T4", "-oX", xml, target]
    code, out, err = run_cmd(cmd, os.path.join(outdir, "nmap_os_detect.txt"))
    print(out or err or f"Exit code: {code}")
    print("\n[Summary]\n" + summarize_nmap(xml, os.path.join(outdir, "SUMMARY_nmap_os_detect.md")))

def task_nmap_udp_top(target: str, outdir: str) -> None:
    banner("[NMAP] Top UDP Ports (Basic)")
    if not ensure_nmap_or_warn():
        return
    xml = os.path.join(outdir, "nmap_udp_top.xml")
    cmd = ["nmap", "-sU", "--top-ports", "10", "-T4", "-oX", xml, target]
    code, out, err = run_cmd(cmd, os.path.join(outdir, "nmap_udp_top.txt"))
    print(out or err or f"Exit code: {code}")
    print("\n[Summary]\n" + summarize_nmap(xml, os.path.join(outdir, "SUMMARY_nmap_udp_top.md")))

def task_nmap_ack_firewall(target: str, outdir: str) -> None:
    banner("[NMAP] ACK Scan (Firewall Rule Check)")
    if not ensure_nmap_or_warn():
        return
    xml = os.path.join(outdir, "nmap_ack.xml")
    cmd = ["nmap", "-sA", "-T4", "-oX", xml, target]
    code, out, err = run_cmd(cmd, os.path.join(outdir, "nmap_ack.txt"))
    print(out or err or f"Exit code: {code}")
    print("\n[Summary]\n" + summarize_nmap(xml, os.path.join(outdir, "SUMMARY_nmap_ack.md")))

def task_nmap_traceroute_version(target: str, outdir: str) -> None:
    banner("[NMAP] Traceroute + Service Version")
    if not ensure_nmap_or_warn():
        return
    xml = os.path.join(outdir, "nmap_traceroute_version.xml")
    cmd = ["nmap", "-sV", "--traceroute", "-T4", "-oX", xml, target]
    code, out, err = run_cmd(cmd, os.path.join(outdir, "nmap_traceroute_version.txt"))
    print(out or err or f"Exit code: {code}")
    print("\n[Summary]\n" + summarize_nmap(xml, os.path.join(outdir, "SUMMARY_nmap_traceroute_version.md")))

# -------------------------------
# Menu & main
# -------------------------------

MENU = """
Choose an action (enter the number):
  1) Ping (connectivity test)
  2) DNS lookup (nslookup/dig)
  3) WHOIS (domain registration data)
  4) Traceroute / Tracert (path to target)
  5) Nmap — Quick scan (top ports)
  6) Nmap — SYN + Service Version detection (-sS -sV)
  7) Nmap — OS detection (-O)
  8) Nmap — Top UDP ports (--top-ports 10)
  9) Nmap — ACK scan (firewall rules)
 10) Nmap — Traceroute + Service Version
 11) Summarize **all** Nmap XML in results folder
 12) Run a beginner-friendly **bundle** (1,2,4,5,6) with summaries
 13) Exit
"""

def summarize_all_in_folder(folder: str) -> None:
    banner("[SUMMARY] Nmap XML files in this folder")
    made_any = False
    for name in os.listdir(folder):
        if name.lower().endswith(".xml") and name.lower().startswith("nmap_"):
            xml = os.path.join(folder, name)
            md  = os.path.join(folder, f"SUMMARY_{os.path.splitext(name)[0]}.md")
            print(f"- Parsing {name} ...")
            summarize_nmap(xml, md)
            made_any = True
    if not made_any:
        print("No Nmap XML files found here yet. Run an Nmap task first.")
    else:
        print("\nSummaries created alongside each XML file (SUMMARY_*.md).")

def beginner_bundle(target: str, outdir: str) -> None:
    """Safe-ish default set for learning purposes (no vuln scripts)."""
    task_ping(target, outdir)
    task_dns_lookup(target, outdir)
    task_traceroute(target, outdir)
    task_nmap_quick_scan(target, outdir)
    task_nmap_service_version(target, outdir)
    summarize_all_in_folder(outdir)

def main():
    banner("Educational Network Recon Tool (Freshman‑Friendly)")
    print("⚠️ Only scan systems you own or have written permission to test.")
    print("This tool saves outputs to a timestamped folder in your current directory.\n")

    # Ask for permission confirmation
    consent = input("Do you have permission to test the target? (yes/no): ").strip().lower()
    if consent not in ("y", "yes"):
        print("Aborting. Please obtain proper authorization first.")
        sys.exit(1)

    target = input("Enter a target (domain like example.com OR IP like 8.8.8.8): ").strip()
    while not target:
        target = input("Target cannot be empty. Please enter a domain or IP: ").strip()

    # Resolve and show IPs (educational)
    ips = resolve_target(target)
    if ips:
        print(f"Resolved IP(s): {', '.join(ips)}")
    else:
        print("Could not resolve IP(s). You may still attempt scans if the target is an IP.")

    outdir = new_output_dir()
    write_text(os.path.join(outdir, "TARGET.txt"), f"Target: {target}\nResolved IPs: {', '.join(ips) if ips else 'N/A'}\n")

    tools_needed = ["ping", "nslookup", "traceroute" if platform.system().lower()!="windows" else "tracert", "whois", "nmap"]
    availability = ensure_tools(tools_needed)
    write_text(os.path.join(outdir, "TOOLS_CHECK.json"), json.dumps(availability, indent=2))
    print("\nTool availability (saved to TOOLS_CHECK.json):")
    for t, ok in availability.items():
        print(f"  - {t:<10} : {'OK' if ok else 'MISSING'}")

    while True:
        print(MENU)
        choice = input("Select an option (1-13): ").strip()
        if choice == "1":
            task_ping(target, outdir)
        elif choice == "2":
            task_dns_lookup(target, outdir)
        elif choice == "3":
            task_whois(target, outdir)
        elif choice == "4":
            task_traceroute(target, outdir)
        elif choice == "5":
            task_nmap_quick_scan(target, outdir)
        elif choice == "6":
            task_nmap_service_version(target, outdir)
        elif choice == "7":
            task_nmap_os_detect(target, outdir)
        elif choice == "8":
            task_nmap_udp_top(target, outdir)
        elif choice == "9":
            task_nmap_ack_firewall(target, outdir)
        elif choice == "10":
            task_nmap_traceroute_version(target, outdir)
        elif choice == "11":
            summarize_all_in_folder(outdir)
        elif choice == "12":
            beginner_bundle(target, outdir)
        elif choice == "13":
            print("Goodbye! Stay ethical and safe.")
            break
        else:
            print("Invalid choice. Please enter a number 1–13.")
        pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)
