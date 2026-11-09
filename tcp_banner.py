"""Connect to one TCP service and read its initial greeting, if it sends one."""

import socket


def read_greeting(host, port, timeout=2):
    """Return a short initial service greeting, or an empty string."""
    with socket.create_connection((host, int(port)), timeout=timeout) as connection:
        connection.settimeout(timeout)
        try:
            return connection.recv(512).decode("utf-8", errors="replace").strip()
        except socket.timeout:
            return ""


def run():
    host = input("Authorized host/IP: ").strip()
    try:
        port = int(input("TCP port: ").strip())
        if not 1 <= port <= 65535:
            raise ValueError("Port must be from 1 to 65535.")
        greeting = read_greeting(host, port)
        print(greeting if greeting else "Connected; service sent no greeting.")
    except (ValueError, OSError) as exc:
        print(f"Check failed: {exc}")


if __name__ == "__main__":
    run()
