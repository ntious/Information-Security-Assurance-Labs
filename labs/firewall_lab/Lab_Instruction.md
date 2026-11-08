# Lab: Firewall Configuration with UFW

**Safety level: 3 — disposable, isolated Ubuntu VM only.**

## Purpose and outcomes

Practice applying a default-deny inbound policy, allowing required test services, and verifying the configured rules. Explain how least privilege and authorization boundaries apply to host firewalls.

## Prerequisites and authorization

- Ubuntu VM that you own or are explicitly authorized to administer.
- Local console access to the VM; do not perform this exercise over a remote session that UFW might interrupt.
- A private, isolated network and a second authorized VM for connection tests.
- VM snapshot or other reset path.

Never use a public IP address or public/shared network as the target. Do not run these commands on a Codespace, shared course host, or production system.

## Setup

From the repository root:

```bash
cd labs/firewall_lab
bash setup.sh
```

The setup script installs UFW, curl, netcat, OpenSSL, and Python 3 on Ubuntu/Debian. Review any package changes before continuing.

## Tasks

1. Record the VM's private lab-network address and current firewall state:

   ```bash
   ip addr
   sudo ufw status verbose
   ```

2. Set the default policies:

   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   ```

3. Add only the ports used for this exercise and the denied examples:

   ```bash
   sudo ufw allow 8000/tcp
   sudo ufw allow 8443/tcp
   sudo ufw deny 21/tcp
   sudo ufw deny 23/tcp
   ```

   Do not add a broad SSH rule for this lab. If an instructor requires a management rule, obtain the exact scope before enabling UFW and retain console access.

4. Enable UFW from the VM console:

   ```bash
   sudo ufw enable
   sudo ufw status numbered
   sudo ufw status verbose
   ```

5. Start the toolkit's HTTP and HTTPS test servers on ports 8000 and 8443. They bind to loopback by default. For peer testing only, type `EXPOSE` at the bind prompt to listen on the lab interface. Do this only on the isolated network. From the second authorized VM, test the target VM's **private lab IP**:

   ```bash
   curl http://<private-lab-vm-ip>:8000
   curl -k https://<private-lab-vm-ip>:8443
   ```

   `-k` is appropriate only for this lab's self-signed test certificate. Stop the servers when testing is complete. If peer connectivity is not needed, keep the default loopback binding.

6. Run the rule checker on the target VM:

   ```bash
   bash ufw_check.sh
   ```

   It checks that UFW is active, the default inbound/outbound policy is correct, and the expected 8000/tcp, 8443/tcp, 21/tcp, and 23/tcp rules exist. A failed connection to an unused port does not, by itself, prove that the firewall blocked it; there may be no service listening.

## Evidence and reflection

Submit the numbered and verbose UFW status, the checker result, and the HTTP/TLS test results. Explain:

1. Why is default deny useful?
2. Why should firewall changes be tested in an isolated VM with console access?
3. What can and cannot be inferred from a failed connection test?
4. Which access rules would be appropriate for a real service, and why should they be narrower than a lab example?

## Cleanup

Use the toolkit's cleanup option to stop its test servers. After saving evidence, disable UFW only on this disposable VM if required by the instructor:

```bash
sudo ufw disable
```

The toolkit stores its generated TLS key and certificate in its private lab data directory. Remove them when they are no longer needed, and do not copy test keys or connection results into public reports.
