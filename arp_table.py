"""Read the operating system's ARP/neighbor cache without changing it."""

import platform
import subprocess


def read_table():
    """Return the platform ARP cache output as text."""
    system = platform.system()
    commands = {
        "Linux": (["ip", "neigh"], ["arp", "-a"]),
        "Windows": (["arp", "-a"],),
        "Darwin": (["arp", "-an"],),
    }.get(system, (["arp", "-a"],))
    errors = []
    for command in commands:
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        except FileNotFoundError:
            errors.append(f"{command[0]} command not found")
            continue
        if result.returncode == 0:
            return result.stdout
        errors.append(result.stderr.strip() or f"{command[0]} returned an error")
    raise RuntimeError("; ".join(errors))


def run():
    try:
        print(f"Local ARP/neighbor cache ({platform.system()}):\n")
        print(read_table() or "No entries found.")
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"Could not read ARP cache: {exc}")


if __name__ == "__main__":
    run()
