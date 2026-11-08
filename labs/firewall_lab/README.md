# Firewall Configuration Lab (Ubuntu + UFW)

**Safety level: 3 — disposable, isolated Ubuntu VM only.** This lab changes host firewall rules and starts network services. Do not run it in Codespaces, on a shared or production host, or on a machine managed over a remote connection that UFW could interrupt. Keep console access and take a VM snapshot before starting.

## Objectives

- Set a default-deny inbound policy.
- Allow the lab's HTTP/TLS test ports and deny two unused example ports.
- Verify rules and controlled service connectivity from an authorized peer.

## Prerequisites

- An Ubuntu VM that you own or are explicitly authorized to administer.
- Console access to the VM and a private, isolated lab network.
- A second authorized VM on that network to test inbound connectivity.

## Quick start

```bash
cd labs/firewall_lab
bash setup.sh
python3 firewall_lab_toolkit.py
```

Follow [Lab_Instruction.md](Lab_Instruction.md) for rule order, service testing, validation, and cleanup. The toolkit's test servers bind to loopback by default. For the isolated-VM peer test only, explicitly type `EXPOSE` at the bind prompt to listen on the lab interface; never expose them to public or shared networks. The checker validates the active firewall policy and expected rules:

```bash
bash ufw_check.sh
```

The checker does not prove that a port is reachable or blocked from a peer. A failed connection can also mean that no service is listening; use the rule output and controlled service tests as separate evidence.

## Cleanup

Stop test servers using the toolkit's cleanup option. After saving your results, disable UFW only on this disposable VM if the instructor requires it. Do not disable firewall protections on any shared or production system.
