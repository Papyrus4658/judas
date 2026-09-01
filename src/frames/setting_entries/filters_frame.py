import tkinter as tk
from tkinter import ttk


class FiltersFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        self._tcp_checked = tk.BooleanVar()
        self._tcp_checked.set(True)
        tcp_check = ttk.Checkbutton(
            self,
            text="TCP",
            variable=self._tcp_checked,
        )

        self._udp_checked = tk.BooleanVar()
        self._udp_checked.set(True)
        udp_check = ttk.Checkbutton(
            self,
            text="UDP",
            variable=self._udp_checked,
        )

        self._sctp_checked = tk.BooleanVar()
        self._sctp_checked.set(True)
        sctp_check = ttk.Checkbutton(
            self,
            text="SCTP",
            variable=self._sctp_checked,
        )

        self._arp_checked = tk.BooleanVar()
        self._arp_checked.set(True)
        arp_check = ttk.Checkbutton(
            self,
            text="ARP",
            variable=self._arp_checked,
        )

        tcp_check.grid(row=1, column=1)
        udp_check.grid(row=1, column=5)
        sctp_check.grid(row=1, column=9)
        arp_check.grid(row=1, column=13)

    @property
    def tcp_checked(self):
        return self._tcp_checked

    @property
    def udp_checked(self):
        return self._udp_checked

    @property
    def sctp_checked(self):
        return self._sctp_checked

    @property
    def arp_checked(self):
        return self._arp_checked
