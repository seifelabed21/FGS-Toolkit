"""Check a short list of common TCP ports on one authorized host."""

import socket

COMMON_PORTS = (21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 389, 443, 445,
                587, 636, 1433, 3306, 3389, 5432, 5985, 8080, 8443)

RISK_NOTES = {
    21: "FTP may send credentials or data without encryption.",
    23: "Telnet is unencrypted and should usually be disabled.",
    445: "SMB is reachable; verify access controls, patching, and scope.",
    3389: "Remote Desktop is reachable; verify exposure and access controls.",
    5985: "WinRM HTTP is reachable; verify it is restricted to trusted networks.",
}


def scan(host, ports=COMMON_PORTS, timeout=0.35):
    """Return ports that accept a TCP connection on host."""
    open_ports = []
    for port in ports:
        try:
            with socket.create_connection((host, int(port)), timeout=timeout):
                open_ports.append(int(port))
        except OSError:
            pass
    return open_ports


def run():
    host = input("Authorized host/IP: ").strip()
    try:
        open_ports = scan(host)
        if not open_ports:
            print("Assessment: no checked ports accepted a TCP connection.")
            print("Decision: NOT VULNERABLE to the checked TCP exposure condition.")
            print("Confidence: low; firewalls and filtered services can produce the same result.")
            return
        print("Reachable TCP ports:", ", ".join(map(str, open_ports)))
        for port in open_ports:
            if port in RISK_NOTES:
                print(f"Potential exposure on {port}: {RISK_NOTES[port]}")
        print("Decision: VULNERABLE to the checked exposure condition.")
        print("Confidence: medium; validate authorization, patching, and service controls manually.")
    except OSError as exc:
        print(f"Scan failed: {exc}")


if __name__ == "__main__":
    run()
