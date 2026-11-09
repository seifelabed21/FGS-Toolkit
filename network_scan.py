"""Find hosts accepting a TCP connection on port 445 in an IPv4 range."""

import ipaddress
import socket


def scan(network, port=445, timeout=0.35):
    """Return responsive IP addresses; limits input to at most 256 addresses."""
    subnet = ipaddress.ip_network(network, strict=False)
    if subnet.version != 4 or subnet.num_addresses > 256:
        raise ValueError("Use an IPv4 network containing at most 256 addresses.")
    alive = []
    for address in subnet.hosts():
        try:
            with socket.create_connection((str(address), port), timeout=timeout):
                alive.append(str(address))
        except OSError:
            pass
    return alive


def run():
    network = input("IPv4 network (up to /24): ").strip()
    try:
        for host in scan(network):
            print(f"{host}: TCP/445 open")
        print("Done. No result does not prove a host is offline.")
    except ValueError as exc:
        print(f"Invalid network: {exc}")


if __name__ == "__main__":
    run()
