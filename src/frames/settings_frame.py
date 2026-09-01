import tkinter as tk
from tkinter import ttk

from scapy.all import ARP, SCTP, TCP, UDP

import constants as c

from .setting__entries import filters_frame as ff
from .setting__entries import iface_frame as sif
from .setting__entries import ip_frame as ipf
from .setting__entries import port_frame as pof


class SettingsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.__iface_frame = sif.IfaceFrame(self)
        self.__port_frame = pof.PortFrame(self)
        self.__ip_frame = ipf.IpFrame(self)
        self.__filters_frame = ff.FiltersFrame(self)

        self.__autoscroll_checked = tk.BooleanVar()
        self.__autoscroll_checked.set(True)
        autoscroll = ttk.Checkbutton(
            self, variable=self.__autoscroll_checked, text=c.SWITCH_AUTOSCROLL
        )

        self.__iface_frame.grid(row=1, column=1, rowspan=5)
        self.__port_frame.grid(row=1, column=5, rowspan=5)
        self.__ip_frame.grid(row=1, column=9, rowspan=5)
        self.__filters_frame.grid(row=1, column=13)
        autoscroll.grid(row=5, column=13)

    def get_iface(self):
        return self.__iface_frame.combo.get()

    def get_port(self):
        return self.__port_frame.spin.get()

    def get_ip(self):
        return self.__ip_frame.entry.get()

    def get_tcp_checked(self):
        return self.__filters_frame.tcp_checked

    def get_udp_checked(self):
        return self.__filters_frame.udp_checked

    def get_sctp_checked(self):
        return self.__filters_frame.sctp_checked

    def get_arp_checked(self):
        return self.__filters_frame.arp_checked

    def get_autoscroll(self):
        return self.__autoscroll_checked.get()

    def check_protocol(self, pkt) -> bool:
        if pkt.haslayer(TCP):
            return self.get_arp_checked()
        if pkt.haslayer(UDP):
            return self.get_udp_checked()
        if pkt.haslayer(SCTP):
            return self.get_sctp_checked()
        if pkt.haslayer(ARP):
            return self.get_arp_checked()
        return False
