#!/usr/bin/env python3

"""
Memory Forensics Toolkit (Volatility 3)
--------------------------------------
Author: I. K. Nti (designed by I. K. Nti)
Date: 2025-09-05
Version: 1.1.0
Dependency: Volatility 3 (tested with v2.26.0)
Python: 3.8+

Usage:
  python3 memforensic_toolkit.py --image /path/to/memdump.raw

Description:
  A menu-driven workflow that guides students from basic to advanced memory
  forensics with Volatility 3. For each action, the tool shows:
    - What it does
    - How to interpret the results (what to look for)
    - Option to save output to a text file
    - Navigation: Continue → Back to menu → Quit
"""

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def build_html_report(out_dir: Path, report_name: str = None):
    r"""Aggregate all .txt outputs in out_dir into a single HTML report.
    The report groups files by timestamp in their name if present.
    r"""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not report_name:
        report_name = f"memforensics_report_{ts}.html"
    report_path = out_dir / report_name

    blocks = []
    for p in sorted(out_dir.glob("*.txt")):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            txt = "(error reading file)"
        blocks.append(f"<section><h3>{p.name}</h3><pre>{html_escape(txt)}</pre></section>")

    html = fr"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Memory Forensics Report</title>
  <style>
    body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Apple Color Emoji"; margin: 2rem; }
    header { margin-bottom: 1.5rem; }
    h1 { margin: 0 0 .25rem 0; }
    .meta { color: #555; }
    section { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; background: #fafafa; }
    pre { white-space: pre-wrap; word-wrap: break-word; }
    footer { margin-top: 2rem; color: #666; font-size: .9rem; }
  </style>
</head>
<body>
  <header>
    <h1>Memory Forensics Report</h1>
    <div class="meta">Generated: {datetime.now().isoformat()}</div>
    <div class="meta">Output Directory: {out_dir}</div>
    <div class="meta">Designed by I. K. Nti</div>
  </header>
  {''.join(blocks) if blocks else '<p><em>No .txt outputs found in the output directory.</em></p>'}
  <footer>Toolkit v1.1.0 • Volatility 3 helper</footer>
</body>
</html>r"""
    report_path.write_text(html, encoding="utf-8")
    print(f"[✓] HTML report written to: {report_path}")
    return report_path

def html_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))

def prompt_yara_path():
    print("\nProvide a YARA rules path. This can be:")
    print("  • a single .yar / .yara file")
    print("  • a directory containing .yar rules (the plugin will walk it)")
    ypath = input("YARA rules path (or leave blank to cancel): ").strip()
    if not ypath:
        return None
    p = Path(ypath).expanduser().resolve()
    if not p.exists():
        print(f"[!] Path not found: {p}")
        return None
    return p


VOL_MIN_PY = (3, 8)  # Vol3 requires Python 3.8+
TESTED_VOL_VERSION = "2.26.0"  # note in README too

def print_header():
    print("\n" + "="*70)
    print(" Memory Forensics Toolkit (Volatility 3)")
    print("="*70)
    print(f"Tested with Volatility 3 v{TESTED_VOL_VERSION} | Python {sys.version.split()[0]}")
    print("Designed by I. K. Nti")
    print("-"*70)

def ask_yes_no(prompt:str, default:str="y")->bool:
    choices = "[Y/n]" if default.lower().startswith("y") else "[y/N]"
    ans = input(f"{prompt} {choices}: ").strip().lower()
    if not ans:
        return default.lower().startswith("y")
    return ans.startswith("y")

def ensure_python_version():
    if sys.version_info < VOL_MIN_PY:
        print(f"[!] Python {VOL_MIN_PY[0]}.{VOL_MIN_PY[1]}+ required for Volatility 3.")
        sys.exit(1)

def detect_volatility():
    """
    Returns a tuple (runner_cmd:list[str], flavor:str)
    flavor in {"vol", "module"}
    """
    vol_path = shutil.which("vol")
    if vol_path:
        return ([vol_path], "vol")
    # Try python -m volatility3
    try:
        subprocess.run([sys.executable, "-m", "volatility3", "--help"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return ([sys.executable, "-m", "volatility3"], "module")
    except Exception:
        return (None, None)

def try_install_volatility():
    print("[*] Volatility 3 not detected.")
    if not ask_yes_no("Do you want to install volatility3 via pip now?", "y"):
        print("[-] Skipping installation. The toolkit cannot run without Volatility 3.")
        sys.exit(1)
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"]
    subprocess.run(cmd, check=False)
    cmd = [sys.executable, "-m", "pip", "install", "volatility3"]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("[!] pip install failed. Please install Volatility 3 manually and re-run.")
        sys.exit(1)

def run_volatility(runner_cmd, image_path, plugin, extra_args=None, output_file=None):
    args = runner_cmd + ["-f", str(image_path), plugin]
    if extra_args:
        args += extra_args
    print(f"\n[+] Running: {' '.join(args)}\n")
    proc = subprocess.run(args, capture_output=True, text=True)
    out = proc.stdout
    err = proc.stderr
    if err.strip():
        print("[!] STDERR:\n", err, sep="")
    if out.strip():
        print(out)
    else:
        print("[!] No output produced.")
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"[✓] Output saved to: {output_file}")
    return out, err, proc.returncode

def prompt_save_output(default_dir):
    if ask_yes_no("Save this output to a file?", "n"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = input(f"Enter filename (default memforensics_{ts}.txt): ").strip()
        if not fname:
            fname = f"memforensics_{ts}.txt"
        out_path = Path(default_dir) / fname
        return out_path
    return None

def show_desc_and_lookfor(desc, look_for):
    print("\n" + "-"*70)
    print(desc)
    print("\nWhat to look for:")
    for li in look_for:
        print(f"  • {li}")
    print("-"*70 + "\n")
    if not ask_yes_no("Proceed with this analysis?", "y"):
        return False
    return True

def next_nav():
    print("\n[C] Continue  [M] Main Menu  [Q] Quit")
    while True:
        choice = input("Select: ").strip().lower()
        if choice in ("c","m","q"):
            return choice
        print("Enter C, M, or Q.")

def basic_menu(runner_cmd, image_path, out_dir):
    while True:
        print("\n--- Basic Analysis ---")
        print("[1] Image Info (windows.info)")
        print("[2] Process List (windows.pslist)")
        print("[3] Process Tree (windows.pstree)")
        print("[4] Network Connections (windows.netscan)")
        print("[B] Back  [Q] Quit")
        sel = input("Choose: ").strip().lower()
        if sel == "1":
            desc = ("Image Info — Detect and display OS/kernel details for the memory image "
                    "(Windows build, arch, symbols).")
            look_for = [
                "Correct OS/arch detection (mismatch ⇒ inaccurate results)",
                "Kernel build and debug symbols availability",
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.info", output_file=outfile)
        elif sel == "2":
            desc = "Process List — Enumerate active processes: PID/PPID/name/exit flags."
            look_for = [
                "Odd process names or misspellings (e.g., 'svhost' vs 'svchost')",
                "Parent/child mismatches (e.g., Word spawning cmd.exe)",
                "Exited/ghost processes still linked"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.pslist", output_file=outfile)
        elif sel == "3":
            desc = "Process Tree — Visualize process hierarchy to spot suspicious parents/children."
            look_for = [
                "Unexpected parents (e.g., explorer.exe spawning powershell.exe)",
                "Orphaned or zombie processes",
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.pstree", output_file=outfile)
        elif sel == "4":
            desc = "Network Connections — List TCP/UDP endpoints and owning processes."
            look_for = [
                "Outbound connections to unknown IPs/domains",
                "Weird ports (1337, 4444), repeated beacons",
                "Long-lived connections from unusual processes",
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.netscan", output_file=outfile)
        elif sel == "b":
            return
        elif sel == "q":
            sys.exit(0)
        else:
            print("Invalid selection.")

def intermediate_menu(runner_cmd, image_path, out_dir):
    while True:
        print("\n--- Intermediate Analysis ---")
        print("[1] DLLs / Modules (windows.dlllist)")
        print("[2] Handles (windows.handles)")
        print("[3] Command Line Args (windows.cmdline)")
        print("[4] Console History (windows.consoles)")
        print("[5] Cmdscan (windows.cmdscan)")
        print("[B] Back  [Q] Quit")
        sel = input("Choose: ").strip().lower()
        if sel == "1":
            desc = "DLLs / Modules — List loaded modules for each process."
            look_for = [
                "Unsigned/unknown DLLs loaded into user processes",
                "DLLs from temp directories or user-writable paths",
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.dlllist", output_file=outfile)
        elif sel == "2":
            desc = "Handles — File/registry/mutex handles kept by processes."
            look_for = [
                "Access to sensitive files/keys (Run keys, Services, SAM)",
                "Unusual named pipes/mutexes indicating malware IPC"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.handles", output_file=outfile)
        elif sel == "3":
            desc = "Command Line Args — Extract process command-line parameters."
            look_for = [
                "Base64 or obfuscated parameters",
                "Suspicious PowerShell flags (-EncodedCommand, -nop, -w hidden)"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.cmdline", output_file=outfile)
        elif sel == "4":
            desc = "Console History — History buffers for console sessions."
            look_for = [
                "Attacker TTPs (whoami, net user, ipconfig, powershell one-liners)"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.consoles", output_file=outfile)
        elif sel == "5":
            desc = "Cmdscan — Parse command history from memory structures."
            look_for = [
                "Recon and execution traces, credential dumping attempts"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.cmdscan", output_file=outfile)
        elif sel == "b":
            return
        elif sel == "q":
            sys.exit(0)
        else:
            print("Invalid selection.")

def advanced_menu(runner_cmd, image_path, out_dir):
    while True:
        print("\n--- Advanced Analysis ---")
        print("[1] Malfind (windows.malfind) [deprecated but useful]")
        print("[2] Hollow Processes (windows.hollowprocesses)")
        print("[3] Process Ghosting (windows.processghosting)")
        print("[4] Services (windows.svclist / svcdiff)")
        print("[5] Registry Quick Wins (amcache, shimcachemem, userassist)")
        print("[6] Dump Process Memory (windows.memmap + procdump)")
        print("[7] YARA Scan (yarascan / windows.vadyarascan)")

        print("[B] Back  [Q] Quit")
        sel = input("Choose: ").strip().lower()
        if sel == "1":
            desc = "Malfind — Identify suspicious/injected memory regions in processes."
            look_for = [
                "Private, RWX pages in user space",
                "PE headers in anonymous mappings",
                "Injected threads in benign processes"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.malfind", output_file=outfile)
        elif sel == "2":
            desc = "Hollow Processes — Detect process hollowing behavior."
            look_for = [
                "Mismatched image path vs. in-memory PE",
                "Suspicious parents spawning system binaries"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.hollowprocesses", output_file=outfile)
        elif sel == "3":
            desc = "Process Ghosting — Identify ghosted processes (deleted image backing)."
            look_for = [
                "Processes backed by SECTION_OBJECTs rather than files",
                "In-memory PE without corresponding on-disk image"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.processghosting", output_file=outfile)
        elif sel == "4":
            desc = "Services — List services and compare against defaults (diff)."
            look_for = [
                "Unexpected autostart services",
                "Services pointing to temp or user directories"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            # Run svclist; svcdiff requires a baseline, so we run svclist by default
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.svclist", output_file=outfile)
        elif sel == "5":
            desc = "Registry Quick Wins — Common persistence & execution artifacts."
            look_for = [
                "Shimcache/Amcache entries for suspicious binaries",
                "UserAssist counts for unusual executables"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            outfile = prompt_save_output(out_dir)
            run_volatility(runner_cmd, image_path, "windows.amcache", output_file=outfile)
            run_volatility(runner_cmd, image_path, "windows.shimcachemem", output_file=outfile)
            run_volatility(runner_cmd, image_path, "windows.userassist", output_file=outfile)
        elif sel == "6":
            desc = "Dump Process — Extract suspicious process memory for offline analysis."
            look_for = [
                "Dump high-risk PIDs from findings above for strings/PE analysis",
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            pid = input("Enter PID to dump: ").strip()
            if not pid.isdigit():
                print("[!] Invalid PID.")
                continue
            outfile = prompt_save_output(out_dir)
            # windows.memdump was v2; in v3, use windows.memmap to identify ranges or use procdump plugin names:
            # windows.dumpfiles dumps files, windows.timers/threads exist. We'll use 'windows.memmap' to map & 'windows.pslist' to confirm,
            # and 'windows.vadwalk' to dump with --dump if supported. Safer: use 'windows.procdump' if available.
            # procdump is not universal; fallback to 'windows.vadwalk --dump'.
            # Try procdump first:
            extra = ["--pid", pid, "--dump"]
            out, _, rc = run_volatility(runner_cmd, image_path, "windows.procdump", extra_args=extra, output_file=outfile)
            if rc != 0 or "No suitable" in out:
                print("[*] procdump failed or unavailable; trying VAD-based dump...")
                run_volatility(runner_cmd, image_path, "windows.vadwalk", extra_args=["--pid", pid, "--dump"], output_file=outfile)

        elif sel == "7":
            desc = "YARA Scan — Search memory for patterns/signatures using your rules."
            look_for = [
                "Rule hits on suspicious strings, packers, C2 indicators",
                "Matches tied to specific PIDs or memory regions"
            ]
            if not show_desc_and_lookfor(desc, look_for): continue
            ypath = prompt_yara_path()
            if not ypath:
                print("[-] YARA scan cancelled.")
                continue

            outfile = prompt_save_output(out_dir)
            # Try windows.vadyarascan first (scans VADs per process), fallback to generic yarascan
            extra_vad = ["--yara-rules", str(ypath)]
            out, _, rc = run_volatility(runner_cmd, image_path, "windows.vadyarascan", extra_args=extra_vad, output_file=outfile)
            if rc != 0:
                print("[*] windows.vadyarascan failed or unavailable; trying generic yarascan...")
                run_volatility(runner_cmd, image_path, "yarascan", extra_args=["--yara-rules", str(ypath)], output_file=outfile)
        elif sel == "b":
            return
        elif sel == "q":
            sys.exit(0)
        else:
            print("Invalid selection.")

def main():
    ensure_python_version()
    parser = argparse.ArgumentParser(description="Volatility 3 Memory Forensics Toolkit (menu-driven)")
    parser.add_argument("--image", "-f", required=False, help="Path to memory dump image")
    parser.add_argument("--out", default="forensics_output", help="Directory to save outputs (optional)")
    args = parser.parse_args()

    print_header()
    runner_cmd, flavor = detect_volatility()
    if not runner_cmd:
        try_install_volatility()
        runner_cmd, flavor = detect_volatility()
        if not runner_cmd:
            print("[!] Volatility 3 still not detected. Exiting.")
            sys.exit(1)

    if not args.image:
        image_path = input("Enter path to memory image: ").strip()
    else:
        image_path = args.image.strip()
    image_path = Path(image_path).expanduser().resolve()
    if not image_path.exists():
        print(f"[!] Image not found: {image_path}")
        sys.exit(1)

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Using Volatility via: {' '.join(runner_cmd)}")
    print(f"[*] Memory image: {image_path}")
    print(f"[*] Output directory: {out_dir}")

    while True:
        print("\nMain Menu")
        print("---------")
        print("[1] Basic Analysis")
        print("[2] Intermediate Analysis")
        print("[3] Advanced Analysis")
        print("[R] Build HTML Report")
        print("[Q] Quit")
        sel = input("Choose: ").strip().lower()
        if sel == "1":
            basic_menu(runner_cmd, image_path, out_dir)
        elif sel == "2":
            intermediate_menu(runner_cmd, image_path, out_dir)
        elif sel == "3":
            advanced_menu(runner_cmd, image_path, out_dir)
        elif sel == "r":
            build_html_report(out_dir)
        elif sel == "q":
            print("Goodbye.")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
