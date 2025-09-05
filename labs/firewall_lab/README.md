# 🛡 Firewall Configuration Lab (Ubuntu + ufw)

**Run ONLY on an Ubuntu VM or local Ubuntu** (not Codespaces).  
You’ll practice real kernel-level firewalling with `ufw` and verify behavior with test services.

## Objectives
- Set default policies (deny incoming / allow outgoing)
- Allow/deny specific ports (22, 80, 443, 21, 23)
- Allow from specific IPs; deny malicious IPs
- Spin up simple HTTP/HTTPS test servers and verify with curl/nc
- (Optional) App-layer allow/deny with Nginx

## Prereqs
Ubuntu 22.04/24.04 with `sudo` access and internet.

## Quick Start
```bash
cd labs/firewall_lab
bash setup.sh           # installs ufw, curl, netcat, openssl, (optional) nginx
python3 firewall_lab_toolkit.py
```
## What to Submit
* Screenshot of ufw status verbose after:
* default deny incoming / allow outgoing
* allows: 22/tcp, 80/tcp, 443/tcp
* denies: 21/tcp, 23/tcp
* Evidence of tests:
* curl http://<public-ip>:80 success
* curl -k https://<public-ip>:443 success (self-signed)
* nc -vz <public-ip> 21 fails
## (Optional) IP allow/deny test results
Run the checker:
  ```bash
bash ufw_check.sh
```
Include the checker’s output in your submission.
## Cleanup
stop background test servers started by the toolkit (menu option 13)
(Optional) disable ufw if this is a shared host
  ```bash
sudo ufw disable
```
Note: Codespaces is great for simulations, but ufw there won’t gate real ingress. Use your university sandbox VM for this lab.

