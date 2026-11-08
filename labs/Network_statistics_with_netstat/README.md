# Netstat Lab Helper — Package

This package contains the menu-driven `netstat_lab_helper.py`, this lab handout, and (where provided) the Task 4 reflection template. Use the helper only in the authorized course sandbox VM.

## How to run
```bash
# if netstat is missing
sudo apt update && sudo apt install -y net-tools

# recommended to see PIDs/program names
sudo -E python3 netstat_lab_helper.py
```
---
## Prerequisites
- Sandbox Ubuntu VM
- Python 3.8+
- `netstat` or `ss` available. If `netstat` is missing, run:
  ```bash
  sudo apt update && sudo apt install -y net-tools
  ```
- Ensure the instructor-provided MySQL container is running if it is required for your course activity. Obtain login details through the approved course platform; do not store them in this repository.

---
## Quick Start
1. Copy `netstat_lab_helper.py` to your VM (e.g., Desktop).
2. Open Terminal and run:
   ```bash
   python3 netstat_lab_helper.py
   ```
3. Use the menu:
   - **1** – Show all TCP/UDP connections with PIDs
   - **2** – Show likely MySQL connections (3306/mysqld)
   - **3/4** – Save full or MySQL‑filtered snapshots to `lab_outputs/`
   - **5** – Terminate a PID (SIGTERM → optional SIGKILL)
   - **6** – Generate Task 4 Reflection template (`Task4_Reflection_Template.txt`)

---
## Common Commands (for context)
- Show all with PIDs (either is fine):
  ```bash
  netstat -tunap
  ss -tunap
  ```
- Narrow to MySQL traffic:
  ```bash
  netstat -tunap | grep 3306
  ss -tunap | grep 3306
  ```
- Terminate by PID (use with caution):
  ```bash
  kill <PID>          # SIGTERM
  kill -9 <PID>       # SIGKILL (only if necessary)
  ```

---
## Evidence for Your Report
- **Screenshots** of Terminal output (Tasks 2–3)
- **Snapshot files** from `./lab_outputs/` (accepted as evidence)
- **Reflection** file (Task 4), completed and included in your submission

> Tip: After you kill a PID, re‑run menu **1** or **2** to verify the connection is gone.

---
## Safety & Ethics
- Only operate on your **VM** and lab containers.
- Killing the wrong PID can disrupt services. Confirm before proceeding.
- When unsure, ask during class or office hours.

---
## Troubleshooting
- **`netstat` not found** → Install `net-tools` (see Prerequisites).
- **No MySQL lines visible** → Confirm `mysqlData` is running in UC Sandbox UI.
- **No PID parsed** → Use menu **1** and inspect the `PID/Program name` column.
- **Permission denied** on `kill` → Try with `sudo` (ask instructor before using `sudo`).

---
## FAQ
**Q: Is using `ss` acceptable if `netstat` isn’t installed?**  
A: Yes. `ss` is the modern replacement; the lab accepts either tool’s output.

**Q: The MySQL PID looks like `docker-proxy`. What do I do?**  
A: That’s part of container networking. Confirm the PID truly relates to the **connection** you intend to terminate before proceeding.

**Q: Do I need to attach both screenshots and snapshot files?**  
A: Screenshots are required; snapshots are helpful supplements.

---

# Canvas‑Ready Student Handout

## Lab: Network Statistics Using `netstat` (Tasks 2–4)

### Learning Outcomes (you’ll practice):
1. Identify and analyze active TCP/UDP connections.
2. Apply network security concepts to spot and terminate a malicious connection.
3. Reflect on why network monitoring matters during incidents.

---
### Setup
1. Sign in to the authorized course sandbox and open its Ubuntu VM.
2. Ensure the instructor-provided MySQL container is running if required.
3. On the VM, open **Terminal** and run:
   ```bash
   sudo apt update && sudo apt install -y net-tools   # if netstat is missing
   ```
4. Download or copy `netstat_lab_helper.py` to your VM and run:
   ```bash
   python3 netstat_lab_helper.py
   ```

> **Screenshot 1 Required:** Show the instructor-provided database container running, if required. Do not include passwords, tokens, or other sensitive information.

---
### Task 2 — Identify Active Connections (Simulated Attack Scenario)
1. In the helper, choose **Option 1** to list **all** active TCP/UDP connections with PIDs; optionally run **Option 2** to focus on likely **MySQL** connections.
2. Confirm the output includes **local/remote addresses**, **state**, and **PID**.
3. Save a snapshot (Option 3 or 4) to `lab_outputs/`.

> **Screenshot 2 Required:** Terminal output showing active connections, including a MySQL connection and its **PID**.

**Guiding Question:** Why is it important to monitor active connections on a server, especially during a potential attack?

---
### Task 3 — Terminate a Malicious Connection (Simulated)
1. Identify the suspected **MySQL** connection’s **PID** from Task 2.
2. In the helper, use **Option 5** to terminate the PID (SIGTERM first; SIGKILL only if needed).
3. Re‑run **Option 1/2** to verify the connection is gone.

> **Screenshot 3 Required:** Evidence that the **kill** was issued and the connection no longer appears in the active list.

**Guiding Question:** What is the significance of identifying and terminating malicious connections in cybersecurity?

---
### Task 4 — Reflection & Analysis
1. Generate the template via **Option 6**.
2. Complete the prompts using your observations (attach with your report):
   - Why monitor active connections during incidents?
   - Which MySQL connection(s) did you observe (addresses/state/PID)?
   - Which PID did you terminate and why?
   - Risks of terminating the wrong PID & how to minimize disruption.
   - Two best practices for continual monitoring & response.

---
### Submission Checklist (Canvas)
- ✅ Screenshot 1: `mysqlData` running + MySQL interface on VM
- ✅ Screenshot 2: Active connections (with MySQL + PID)
- ✅ Screenshot 3: Termination evidence & post‑check
- ✅ Completed Reflection (`Task4_Reflection_Template.txt` contents or pasted text)
- ✅ Optional: Include snapshot files from `./lab_outputs/`

---
### Grading Rubric (Summary)
- **Excellent**: Thorough, accurate outputs & insights; all evidence provided.
- **Good**: Solid work with minor omissions.
- **Needs Improvement**: Significant gaps/errors; unclear reasoning.
- **No Submission**: Missing or does not meet basic requirements.

---
### Safety Notes
- Operate **only** on your lab VM/containers.
- Confirm the **correct PID** before killing; when unsure, ask.
- Re‑verify connections after actions and document evidence.

---
### Instructor Notes (Optional to include in Canvas)
- Accept `ss` outputs as equivalent to `netstat`.
- If container UI is preferred to CLI for MySQL verification, that’s fine; require the **PID** to be documented in evidence.
- Encourage students to annotate screenshots (PID circled, timestamp visible).
## Notes
- Option 2 now checks ports **3306** and **33060** and includes a **deep hunt** for
  LISTEN + UNIX sockets, so you always have something useful to document.
- If you see no TCP entries, MySQL may be **UNIX-socket only**. Use the deep hunt
  output or open a TCP client (`mysql -h 127.0.0.1 -P 3306 -u root -p`) and re-check.