# FGS Toolkit

A simple, modular Python CLI for authorized internal network assessments. `main.py` displays the menu. Each tool is an independent file with a reusable function and can also be run directly.

<img width="897" height="467" alt="image" src="https://github.com/user-attachments/assets/db738fdc-a63e-42bb-b2f6-128dae4f4d44" />


## Safety and use restrictions

Use only on systems and networks you own or are explicitly authorized to assess.

- Do not use this toolkit to disrupt services, evade detection, spoof traffic, flood networks, exploit systems, or access data without permission.
- The toolkit performs bounded, defensive checks only. It does not send floods, craft spoofed packets, exploit vulnerabilities, or attempt credential attacks.
- Keep scans within written scope and approved rate, timing, and target limits.
- Results are indicators for authorized review, not proof of security or compromise.

These restrictions prevent harm to infrastructure, service outages, unauthorized access, and inaccurate security conclusions.

## Install on Linux

After cloning the repository, from its project directory run:

```bash
chmod +x install.sh
./install.sh
fgs-toolkit
```

The installer uses `~/.local/share/fgs-toolkit` and `~/.local/bin`; it does not need root access. If `fgs-toolkit` is not found, add `export PATH="$HOME/.local/bin:$PATH"` to your shell profile and open a new terminal.

## Run from source

Requires Python 3.9 or newer:

```bash
cd FGS-Toolkit
python main.py
```

Optional dependencies for packet capture and AD DNS lookups:

```bash
python -m pip install scapy dnspython
```

## Tools

1. `network_scan.py` - checks TCP/445 on an IPv4 range up to 256 addresses.
2. `port_scan.py` - checks common TCP ports on one host and flags potentially risky exposed services for manual validation.
3. `dns_lookup.py` - resolves a hostname.
4. `packet_sniffer.py` - short packet metadata capture; does not show payloads.
5. `mac_spoof_check.py` - performs a read-only ARP-cache consistency check and reports a bounded vulnerable/not-vulnerable decision with confidence.
6. `syn_flood_check.py` - checks local Linux SYN-cookie and backlog hardening and reports a bounded vulnerable/not-vulnerable decision; sends no flood traffic.
7. `assessment.py` - checks a single host or IPv4 subnet up to 16 addresses and writes `fgs-assessment-report.txt`.
8. `ad_dns.py` - looks up common AD LDAP/Kerberos DNS service records.

## Assessment flow

Confirm written scope and timing. Inventory approved hosts and services. Review DNS and AD service records. Validate observations with the system owner, then report evidence, impact, confidence, limits, and remediation. The automated report is an inventory note, not a complete penetration test or proof of vulnerabilities.

The toolkit uses ordinary network connections and may be visible in monitoring logs. The spoofing and SYN-flood options are defensive, read-only checks; they do not perform the attacks. It contains no stealth, evasion, exploitation, credential attacks, spoofing, packet crafting, or flooding. A `VULNERABLE` result means the bounded condition was observed; `NOT VULNERABLE` means it was not observed, not that the host is secure. Confidence and limitations are printed so results can be validated manually. Use only on systems you own or have explicit permission to assess.
