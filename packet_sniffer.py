"""Short packet metadata capture (optional Scapy; no payload output)."""


def capture(seconds=10, interface=None):
    """Return source/destination/protocol/length rows for a short capture."""
    if not 1 <= int(seconds) <= 30:
        raise ValueError("Capture duration must be from 1 to 30 seconds.")
    try:
        from scapy.all import IP, TCP, UDP, sniff
    except ImportError as exc:
        raise RuntimeError("Install optional dependency: python -m pip install scapy") from exc
    packets = sniff(timeout=int(seconds), store=True, iface=interface)
    rows = []
    for packet in packets:
        if IP in packet:
            protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else str(packet[IP].proto)
            rows.append((packet[IP].src, packet[IP].dst, protocol, len(packet)))
    return rows


def run():
    try:
        seconds = int(input("Capture duration in seconds (1-30): ").strip())
        print("Capturing packet metadata only. Elevated privileges may be required.")
        for source, destination, protocol, length in capture(seconds):
            print(f"{source} -> {destination} protocol={protocol} bytes={length}")
    except ValueError as exc:
        print(f"Invalid duration: {exc}")
    except RuntimeError as exc:
        print(exc)
    except OSError as exc:
        print(f"Capture failed (check adapter/privileges): {exc}")


if __name__ == "__main__":
    run()
