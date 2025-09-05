# Memory Forensics Toolkit (Volatility 3)

**Designed by I. K. Nti**  
Tested on **Volatility 3 v2.26.0** (as of 2025-09-05)

## ⚠️ Educational Use & Safety
- This toolkit is for **educational and research** purposes.  
- **Only analyze memory images that you own or have explicit written authorization to inspect.**  
- Run in a **virtual machine** or on **your own lab network**. Do **not** run against third‑party systems without permission.

## ✨ What It Does
- Checks for **Volatility 3** and offers to install if missing.
- Guides you through **Basic → Intermediate → Advanced** memory analysis with clear **“what to look for”** notes.
- Saves outputs to text files on demand.

## ✅ Requirements
- Python **3.8+**
- Volatility 3 (pip package `volatility3`)
- Windows memory images are supported by the menu options included here.

## 📦 Install Volatility 3
```bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install volatility3
```

Alternatively, use `vol` standalone binaries from the Volatility Foundation.

## 🚀 Usage
```bash
python3 memforensic_toolkit.py --image /path/to/memdump.raw
# Optional: choose output directory
python3 memforensic_toolkit.py --image /path/to/memdump.raw --out results/
```

If `--image` is omitted, you’ll be prompted interactively.

## 🧭 Menu Overview
**Basic**
- `windows.info` — detect OS/arch
- `windows.pslist`, `windows.pstree` — process inventory
- `windows.netscan` — sockets & endpoints

**Intermediate**
- `windows.dlllist` — loaded modules
- `windows.handles` — files/registry/mutexes
- `windows.cmdline`, `windows.consoles`, `windows.cmdscan` — execution traces

**Advanced**
- `windows.malfind` — injected code regions (deprecated but still useful)
- `windows.hollowprocesses`, `windows.processghosting` — stealthy process techniques
- `windows.svclist` — services
- `windows.amcache`, `windows.shimcachemem`, `windows.userassist` — fast registry triage
- Process dumping: `windows.procdump` (fallback `windows.vadwalk --dump`)

> Note: Some plugins require specific symbol tables or work best on specific Windows builds.

## 📝 Version Notes
- Toolkit developed and tested with **Volatility 3 v2.26.0** (GitHub latest release at time of writing).  
- Minimum Python supported by Volatility 3 is **3.8**.

## 🙌 Credit
- Volatility Framework by the **Volatility Foundation**.
- Course toolkit and documentation **designed by I. K. Nti**.
