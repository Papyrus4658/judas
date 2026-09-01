import queue
from datetime import datetime

from scapy.all import ARP, IP, SCTP, TCP, UDP, IPv6

import constants as c


class Capture:
    def __init__(self):
        pass

    def create_record(self, pkt):
        size = len(pkt)

        if pkt.haslayer(TCP):
            protocol = "TCP"
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            flags = str(pkt[TCP].flags)
        elif pkt.haslayer(UDP):
            protocol = "UDP"
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport
            flags = ""
        elif pkt.haslayer(SCTP):
            protocol = "SCTP"
            sport = pkt[SCTP].sport
            dport = pkt[SCTP].dport
            flags = ""
        elif pkt.haslayer(ARP):
            protocol = "ARP"
            sport = pkt[ARP].psrc
            dport = pkt[ARP].pdst
            flags = f"op={pkt[ARP].op}"
        else:
            return

        if pkt.haslayer(IP):
            src = pkt[IP].src
            dst = pkt[IP].dst
        elif pkt.haslayer(IPv6):
            src = pkt[IPv6].src
            dst = pkt[IPv6].dst
        else:
            return

        now = datetime.now(c.LOCAL_TZ).time().strftime(c.TIME_FORMAT)

        return (now, protocol, src, sport, dst, dport, flags, size)
