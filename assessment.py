"""Run a small, bounded network inventory and save a plain-text report."""

from datetime import datetime, timezone
from pathlib import Path

import ipaddress

import port_scan

ASSESSMENT_PORTS = (22, 53, 80, 135, 139, 443, 445, 3389)


def assess(target):
    """Return host and open-port observations for a single IP or small subnet."""
    network = ipaddress.ip_network(target, strict=False)
    if network.version != 4 or network.num_addresses > 16:
        raise ValueError("For safety, use IPv4 targets containing at most 16 addresses (/28 or smaller).")
    lines = [
        "FGS Toolkit - authorized assessment notes",
        f"UTC time: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Scope: {network}",
        "Method: ordinary TCP connect checks; results require manual validation.",
        "",
    ]
    for address in network.hosts():
        host = str(address)
        found = port_scan.scan(host, ASSESSMENT_PORTS)
        if found:
            lines.append(f"{host}: open TCP ports {', '.join(map(str, found))}")
    if len(lines) == 5:
        lines.append("No responding hosts/services found in this limited check.")
    return "\n".join(lines) + "\n"


def run():
    target = input("Authorized IPv4 address or small subnet (max 16 IPs): ").strip()
    try:
        report = assess(target)
        path = Path("fgs-assessment-report.txt")
        path.write_text(report, encoding="utf-8")
        print(report)
        print(f"Saved report: {path.resolve()}")
    except (ValueError, OSError) as exc:
        print(f"Assessment stopped: {exc}")


if __name__ == "__main__":
    run()
