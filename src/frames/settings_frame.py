import tkinter as tk
from tkinter import ttk

from scapy.all import ARP, SCTP, TCP, UDP, scapy

import constants as c

from .setting_entries import filters_frame as filters_f
from .setting_entries import iface_frame as iface_f
from .setting_entries import ip_frame as ip_f
from .setting_entries import port_frame as port_f


class SettingsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self._iface_frame = iface_f.IfaceFrame(self)
        self._port_frame = port_f.PortFrame(self)
        self._ip_frame = ip_f.IpFrame(self)
        self._filters_frame = filters_f.FiltersFrame(self)

        self._autoscroll_checked = tk.BooleanVar()
        self._autoscroll_checked.set(True)
        autoscroll = ttk.Checkbutton(
            self, variable=self._autoscroll_checked, text=c.SWITCH_AUTOSCROLL
        )

        self._iface_frame.grid(row=1, column=1, rowspan=5)
        self._port_frame.grid(row=1, column=5, rowspan=5)
        self._ip_frame.grid(row=1, column=9, rowspan=5)
        self._filters_frame.grid(row=1, column=13)
        autoscroll.grid(row=5, column=13)

    def get_iface(self):
        return self._iface_frame.combo.get()

    def get_port(self):
        return self._port_frame.spin.get()

    def get_ip(self):
        return self._ip_frame.entry.get()

    def get_tcp_checked(self):
        return self._filters_frame.tcp_checked

    def get_udp_checked(self):
        return self._filters_frame.udp_checked

    def get_sctp_checked(self):
        return self._filters_frame.sctp_checked

    def get_arp_checked(self):
        return self._filters_frame.arp_checked

    def get_autoscroll(self):
        return self._autoscroll_checked.get()

    def check_protocol(self, pkt):
        if pkt.haslayer(TCP):
            return self.get_tcp_checked()
        if pkt.haslayer(UDP):
            return self.get_udp_checked()
        if pkt.haslayer(SCTP):
            return self.get_sctp_checked()
        if pkt.haslayer(ARP):
            return self.get_arp_checked()
        return False
