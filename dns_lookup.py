"""Resolve a hostname with Python's standard library."""

import socket


def lookup(host):
    """Return unique IP addresses resolved for host."""
    return sorted({row[4][0] for row in socket.getaddrinfo(host, None)})


def run():
    host = input("Hostname: ").strip()
    try:
        for address in lookup(host):
            print(address)
    except OSError as exc:
        print(f"Lookup failed: {exc}")


if __name__ == "__main__":
    run()
