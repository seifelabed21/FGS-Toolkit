"""Look up Active Directory LDAP/Kerberos service records (optional dnspython)."""


def lookup(domain):
    """Return SRV records for common AD LDAP and Kerberos DNS names."""
    try:
        import dns.resolver
    except ImportError as exc:
        raise RuntimeError("Install optional dependency: python -m pip install dnspython") from exc
    records = {}
    for name in (f"_ldap._tcp.dc._msdcs.{domain}", f"_kerberos._tcp.{domain}"):
        try:
            records[name] = [
                {"target": str(row.target), "port": row.port, "priority": row.priority}
                for row in dns.resolver.resolve(name, "SRV", lifetime=3)
            ]
        except Exception as exc:
            records[name] = f"No answer: {exc}"
    return records


def run():
    try:
        for name, records in lookup(input("AD DNS domain (example.local): ").strip(" ." )).items():
            print(f"\n{name}")
            if isinstance(records, str):
                print(" ", records)
            else:
                for record in records:
                    print(" ", record)
    except RuntimeError as exc:
        print(exc)


if __name__ == "__main__":
    run()
