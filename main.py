#!/usr/bin/env python3
"""FGS Toolkit menu. Run with: python main.py"""

import ad_dns
import assessment
import dns_lookup
import mac_spoof_check
import network_scan
import packet_sniffer
import port_scan
import syn_flood_check


TOOLS = {
    "1": ("Network discovery (TCP/445)", network_scan.run),
    "2": ("Common service exposure check", port_scan.run),
    "3": ("DNS lookup", dns_lookup.run),
    "4": ("Packet metadata sniffer (optional Scapy)", packet_sniffer.run),
    "5": ("Check local ARP cache for spoofing indicators", mac_spoof_check.run),
    "6": ("Check local SYN flood protection settings", syn_flood_check.run),
    "7": ("Scoped assessment and report", assessment.run),
    "8": ("Active Directory DNS discovery (optional dnspython)", ad_dns.run),
}


def main():
    print(r"""
 _______  _______  _______   _________ _______  _______  _        _       __________________
(  ____ \(  ____ \(  ____ \  \__   __/(  ___  )(  ___  )( \      | \    /\\__   __/\__   __/
| (    \/| (    \/| (    \/     ) (   | (   ) || (   ) || (      |  \  / /   ) (      ) (   
| (__    | |      | (_____      | |   | |   | || |   | || |      |  (_/ /    | |      | |   
|  __)   | | ____ (_____  )     | |   | |   | || |   | || |      |   _ (     | |      | |   
| (      | | \_  )      ) |     | |   | |   | || |   | || |      |  ( \ \    | |      | |   
| )      | (___) |/\____) |     | |   | (___) || (___) || (____/\|  /  \ \___) (___   | |   
|/       (_______)\_______)     )_(   (_______)(_______)(_______/|_/    \/\_______/   )_(   
                                                                                            
""")
    print("Authorized internal assessment helpers\n")
    while True:
        for key, (label, _) in TOOLS.items():
            print(f"{key}. {label}")
        print("0. Exit")
        choice = input("\nSelect a tool: ").strip()
        if choice == "0":
            print("Goodbye.")
            return
        if choice in TOOLS:
            print()
            TOOLS[choice][1]()
        else:
            print("Choose one of the listed options.")
        print()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nStopped.")
