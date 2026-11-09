"""Look for conflicting IP-to-MAC entries in the local neighbor cache."""

import re

import arp_table

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
MAC_RE = re.compile(r"\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b")


def find_conflicts(cache_text):
    """Return IPs associated with multiple MACs in supplied ARP output."""
    mappings = {}
    for line in cache_text.splitlines():
        ip_match = IP_RE.search(line)
        mac_match = MAC_RE.search(line)
        if ip_match and mac_match:
            ip = ip_match.group(0)
            mac = mac_match.group(0).lower().replace("-", ":")
            mappings.setdefault(ip, set()).add(mac)
    return {ip: sorted(macs) for ip, macs in mappings.items() if len(macs) > 1}


def analyze(cache_text):
    """Return a bounded ARP-spoofing assessment from the supplied cache text."""
    conflicts = find_conflicts(cache_text)
    if conflicts:
        return {
            "decision": "VULNERABLE",
            "confidence": "medium",
            "evidence": conflicts,
            "analysis": (
                "The local cache contains an IP address associated with multiple "
                "MAC addresses. This is consistent with ARP spoofing, but can also "
                "occur during legitimate failover or address reassignment."
            ),
        }
    return {
        "decision": "NOT VULNERABLE",
        "confidence": "low",
        "evidence": {},
        "analysis": (
            "No conflicting IP/MAC entries were observed in the current local "
            "cache. This does not detect every ARP-spoofing technique."
        ),
    }


def run():
    try:
        result = analyze(arp_table.read_table())
    except (OSError, RuntimeError) as exc:
        print(f"Could not inspect the local neighbor cache: {exc}")
        return
    print(f"Decision: {result['decision']} (confidence: {result['confidence']})")
    print(f"Analysis: {result['analysis']}")
    if result["evidence"]:
        print("Evidence: an IP maps to multiple MAC addresses:")
        for ip, macs in result["evidence"].items():
            print(f"  {ip}: {', '.join(macs)}")


if __name__ == "__main__":
    run()
