#!/usr/bin/env python3
import os
import re
import shlex
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

SUDO = "sudo "
PIDS_FILE = Path("/tmp/firewall_lab_toolkit.pids")
CERT_FILE = Path("./cert.pem")
KEY_FILE = Path("./key.pem")

def run(cmd, check=False, capture=False):
    """Run a shell command; optionally capture output and raise on error."""
    if isinstance(cmd, str):
        cmd_list = shlex.split(cmd)
    else:
        cmd_list = cmd
    try:
        if capture:
            out = subprocess.run(cmd_list, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check)
            return out.stdout
        else:
            return subprocess.run(cmd_list, text=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {' '.join(cmd_list)}")
        if hasattr(e, 'stdout') and e.stdout:
            print(e.stdout)
        elif e.stderr:
            print(e.stderr)
        return None

def which(binary):
    return run(f"bash -lc 'command -v {shlex.quote(binary)}'", capture=True)

def ensure_ufw():
    if not which("ufw"):
        print("[i] ufw not found. Installing...")
        run(SUDO + "apt-get update -y")
        run(SUDO + "apt-get install -y ufw")
    else:
        print("[✓] ufw is installed.")

def show_status():
    print(run(SUDO + "ufw status verbose", capture=True))

def enable_firewall():
    print("[i] Enabling ufw (will set to enabled if not already).")
    run(SUDO + "ufw --force enable")
    show_status()

def set_default_policies():
    print("[i] Setting default policies: deny incoming, allow outgoing.")
    run(SUDO + "ufw default deny incoming")
    run(SUDO + "ufw default allow outgoing")
    show_status()

def allow_port():
    port = input("Enter port number to ALLOW (e.g., 22 or 443): ").strip()
    proto = input("Protocol [tcp/udp] (default tcp): ").strip().lower() or "tcp"
    if not port.isdigit() or proto not in ("tcp", "udp"):
        print("[!] Invalid input.")
        return
    run(f"{SUDO}ufw allow {port}/{proto}")
    show_status()

def deny_port():
    port = input("Enter port number to DENY (e.g., 21 or 23): ").strip()
    proto = input("Protocol [tcp/udp] (default tcp): ").strip().lower() or "tcp"
    if not port.isdigit() or proto not in ("tcp", "udp"):
        print("[!] Invalid input.")
        return
    run(f"{SUDO}ufw deny {port}/{proto}")
    show_status()

def allow_from_ip():
    ip = input("Allow from IP (e.g., 192.0.2.10): ").strip()
    port = input("to port (e.g., 22): ").strip()
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip) or not port.isdigit():
        print("[!] Invalid IP or port.")
        return
    run(f"{SUDO}ufw allow from {ip} to any port {port}")
    show_status()

def deny_from_ip():
    ip = input("Deny from IP (e.g., 203.0.113.1): ").strip()
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        print("[!] Invalid IP.")
        return
    run(f"{SUDO}ufw deny from {ip}")
    show_status()

def list_numbered():
    print(run(SUDO + "ufw status numbered", capture=True))

def delete_rule_by_number():
    list_numbered()
    num = input("Enter rule number to delete (as shown in [ # ]): ").strip()
    if not num.isdigit():
        print("[!] Invalid number.")
        return
    # Use `yes` to auto-confirm deletion
    run(f"bash -lc \"yes | {SUDO}ufw delete {num}\"")
    show_status()

def show_ip_info():
    print("[i] IP info (ip addr):")
    print(run("ip addr", capture=True))
    if which("ss"):
        print("[i] Listening sockets (ss -tulpen):")
        print(run("ss -tulpen", capture=True))
    else:
        print(run("netstat -tulpen", capture=True) or "")

def _write_pid(pid):
    existing = set()
    if PIDS_FILE.exists():
        existing = set(int(x.strip()) for x in PIDS_FILE.read_text().splitlines() if x.strip().isdigit())
    existing.add(pid)
    PIDS_FILE.write_text("\n".join(str(p) for p in sorted(existing)))

def _kill_pids():
    if not PIDS_FILE.exists():
        print("[i] No background server PIDs tracked.")
        return
    pids = [int(x) for x in PIDS_FILE.read_text().splitlines() if x.strip().isdigit()]
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[✓] Stopped PID {pid}")
        except ProcessLookupError:
            print(f"[i] PID {pid} not running.")
    try:
        PIDS_FILE.unlink()
    except FileNotFoundError:
        pass

def start_http_server():
    port = input("HTTP port (default 8000): ").strip() or "8000"
    if not port.isdigit():
        print("[!] Invalid port.")
        return
    print(f"[i] Starting Python HTTP server on :{port} (background).")
    proc = subprocess.Popen([sys.executable, "-m", "http.server", port], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _write_pid(proc.pid)
    print(f"[✓] HTTP server PID {proc.pid}. Try: curl http://<public-ip>:{port}")

def _ensure_self_signed_cert():
    if CERT_FILE.exists() and KEY_FILE.exists():
        return
    print("[i] Generating self-signed TLS cert (1-day).")
    run(f"openssl req -x509 -newkey rsa:2048 -keyout {KEY_FILE} -out {CERT_FILE} -days 1 -nodes -subj /CN=localhost")

def start_https_server():
    port = input("HTTPS port (default 8443): ").strip() or "8443"
    if not port.isdigit():
        print("[!] Invalid port.")
        return
    _ensure_self_signed_cert()
    # Launch a tiny HTTPS server using Python stdlib in background
    code = f"""
import http.server, ssl, socketserver
handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", {int(port)}), handler) as httpd:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile="{CERT_FILE}", keyfile="{KEY_FILE}")
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print("Serving HTTPS on {int(port)}")
    httpd.serve_forever()
"""
    proc = subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _write_pid(proc.pid)
    print(f"[✓] HTTPS server PID {proc.pid}. Try: curl -k https://<public-ip>:{port}")

def stop_test_servers():
    _kill_pids()

def quick_test():
    host = input("Target host/IP (default: this VM public IP or localhost): ").strip()
    if not host:
        # Try to guess a non-loopback IP
        host = "127.0.0.1"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            host = s.getsockname()[0]
            s.close()
        except Exception:
            pass
    proto = input("Protocol [http/https/custom] (default http): ").strip().lower() or "http"
    port = input("Port (blank to use 80/443 for http/https): ").strip()
    if not port:
        port = "443" if proto == "https" else "80"
    if not port.isdigit():
        print("[!] Invalid port.")
        return
    if proto in ("http", "https"):
        flag = "-k " if proto == "https" else ""
        print(run(f"curl -I {flag}{proto}://{host}:{port}", capture=True))
    else:
        print(run(f"nc -vz {host} {port}", capture=True))

def install_nginx_demo():
    print("[i] Installing nginx (app-layer allow/deny demo).")
    run(SUDO + "apt-get update -y")
    run(SUDO + "apt-get install -y nginx")
    # Minimal restrictive server on 8080
    conf = r"""
server {
    listen 8080;
    location / {
        allow 203.0.113.10;    # example allowed IP
        deny all;
        return 403;
    }
}
"""
    Path("/tmp/allowlist.conf").write_text(conf.strip()+"\n")
    run(SUDO + "mv /tmp/allowlist.conf /etc/nginx/conf.d/allowlist.conf")
    # Reload nginx (handle both systemd and non-systemd)
    run(SUDO + "nginx -t")
    if which("systemctl"):
        run(SUDO + "systemctl restart nginx")
    else:
        run(SUDO + "nginx -s reload || true")
    print("[✓] Nginx allow/deny demo listening on :8080. Try curl http://<public-ip>:8080")

def banner():
    print("""
=============================================
   Firewall Lab Toolkit (Ubuntu + ufw)
=============================================
[1]  Show IP and listening ports
[2]  Install/verify ufw
[3]  Enable ufw
[4]  Set default policies (deny incoming, allow outgoing)
[5]  Allow a port
[6]  Deny a port
[7]  Allow from IP to port
[8]  Deny from IP
[9]  List rules (numbered)
[10] Delete rule by number
[11] Start HTTP test server (background)
[12] Start HTTPS test server (background, self-signed)
[13] Stop all test servers
[14] Quick connectivity test (curl/nc)
[15] Install Nginx allow/deny demo (app-layer)
[0]  Exit
""")

def main():
    # Environment advisory
    if os.environ.get("CODESPACES") == "true":
        print("[!] Detected GitHub Codespaces. Note: ufw will not control platform ingress here. Use for syntax/demo only.")
    while True:
        banner()
        choice = input("Select an option: ").strip()
        if choice == "1":
            show_ip_info()
        elif choice == "2":
            ensure_ufw()
        elif choice == "3":
            ensure_ufw(); enable_firewall()
        elif choice == "4":
            ensure_ufw(); set_default_policies()
        elif choice == "5":
            ensure_ufw(); allow_port()
        elif choice == "6":
            ensure_ufw(); deny_port()
        elif choice == "7":
            ensure_ufw(); allow_from_ip()
        elif choice == "8":
            ensure_ufw(); deny_from_ip()
        elif choice == "9":
            ensure_ufw(); list_numbered()
        elif choice == "10":
            ensure_ufw(); delete_rule_by_number()
        elif choice == "11":
            start_http_server()
        elif choice == "12":
            start_https_server()
        elif choice == "13":
            stop_test_servers()
        elif choice == "14":
            quick_test()
        elif choice == "15":
            install_nginx_demo()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("[!] Invalid option.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    shutil_available = hasattr(__import__('shutil'), 'which')  # pyright: ignore[reportUndefinedVariable]
    if not shutil_available:
        pass
    main()
