# Lab: Memory Forensics with Volatility 3 (Basic → Advanced)

**Objective:** Learn a practical workflow for Windows memory forensics using Volatility 3 by running progressively deeper analyses and interpreting the results.

---

## Prerequisites
- Python 3.8+
- Volatility 3 installed (`pip install volatility3`) or `vol` binary available
- A Windows memory image (e.g., `.raw`, `.mem`, `.dmp`)

---

## Quick Start
1. Place your memory image in a working folder.
2. Run the toolkit:
   ```bash
   python3 memforensic_toolkit.py --image /path/to/memdump.raw
   ```
3. Choose **Basic**, then work through **Intermediate** and **Advanced** menus.
4. When prompted, **save outputs** for later documentation.

---

## Suggested Workflow
### 1) Basic Triage
- **Image Info (`windows.info`)**: Confirm OS/arch; ensure symbols load correctly.
- **Processes (`windows.pslist` / `windows.pstree`)**: Establish normal vs. suspicious activity.
- **Network (`windows.netscan`)**: Note any suspicious endpoints/ports.

### 2) Enrichment
- **DLLs (`windows.dlllist`)**: Look for unsigned or odd-path modules.
- **Handles (`windows.handles`)**: Inspect sensitive files/registry handles.
- **Execution Artifacts (`windows.cmdline`, `windows.consoles`, `windows.cmdscan`)**: Recover operator commands.

### 3) Deep Detections
- **Injected Code (`windows.malfind`)**: Flag RWX anonymous mappings, PE headers in RAM.
- **Process Masquerade (`windows.hollowprocesses`, `windows.processghosting`)**: Detect stealth techniques.
- **Services (`windows.svclist`)**: Identify malicious persistence as a service.
- **Registry Fast Triage (`windows.amcache`, `windows.shimcachemem`, `windows.userassist`)**: Corroborate execution.

### 4) Carving & Export
- **Dump process memory** using `windows.procdump --pid <PID> --dump`
  - If unavailable, fallback: `windows.vadwalk --pid <PID> --dump`
- Analyze dumps with **strings**, **pefile**, **yara**, or a sandbox (safely!).

---

## Reporting Tips
- For every suspicious finding, record:
  - **Plugin used + parameters**
  - **Evidence snippet (copy relevant lines)**
  - **Reasoning** (why it’s suspicious)
  - **Next action** (dump, hash, pivot to other artifacts)
- Keep a **timeline**: commands discovered → processes → network → persistence.

---

## Ethics & Safety
- Use only **authorized** images.
- Prefer analyzing in a **VM** with network isolation.
- Do not open dumped binaries on a host without proper controls.

---

## Designed by
**I. K. Nti** — Course toolkit author.
