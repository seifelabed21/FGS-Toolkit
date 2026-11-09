"""Read Linux SYN-cookie and connection-backlog settings; sends no test traffic."""

from pathlib import Path
import platform


DEFAULT_ROOT = Path("/proc/sys/net/ipv4")


def read_settings(root=DEFAULT_ROOT):
    """Read local Linux SYN protection values from procfs."""
    if platform.system() != "Linux":
        raise RuntimeError("This read-only configuration check currently supports Linux only.")
    root = Path(root)
    paths = {
        "tcp_syncookies": root / "tcp_syncookies",
        "tcp_max_syn_backlog": root / "tcp_max_syn_backlog",
        "somaxconn": root.parent / "core" / "somaxconn",
    }
    values = {}
    for name, path in paths.items():
        values[name] = int(path.read_text(encoding="ascii").strip())
    return values


def analyze(settings):
    """Return a bounded SYN-protection decision from local settings."""
    result = []
    if settings["tcp_syncookies"] == 1:
        result.append("SYN cookies: enabled (mitigation observed).")
        decision = "NOT VULNERABLE"
        confidence = "medium"
    else:
        result.append("SYN cookies: disabled (review local hardening policy).")
        decision = "VULNERABLE"
        confidence = "medium"
    result.append(f"TCP SYN backlog: {settings['tcp_max_syn_backlog']} (review against host workload/policy).")
    result.append(f"Listener backlog ceiling: {settings['somaxconn']} (review against host workload/policy).")
    result.append(
        f"Decision: {decision} (confidence: {confidence}) for the basic SYN-cookie "
        "hardening check."
    )
    result.append(
        "Analysis: this is a read-only configuration result; no SYN flood or "
        "incomplete-handshake traffic was sent."
    )
    return result


def run():
    try:
        for line in analyze(read_settings()):
            print(line)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Could not read SYN protection settings: {exc}")


if __name__ == "__main__":
    run()
