import tkinter as tk
from tkinter import ttk


class FiltersFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        self.__tcp_checked = tk.BooleanVar()
        self.__tcp_checked.set(True)
        tcp_check = ttk.Checkbutton(self, text="TCP", variable=self.__tcp_checked)

        self.__udp_checked = tk.BooleanVar()
        self.__udp_checked.set(True)
        udp_check = ttk.Checkbutton(self, text="UDP", variable=self.__udp_checked)

        self.__sctp_checked = tk.BooleanVar()
        self.__sctp_checked.set(True)
        sctp_check = ttk.Checkbutton(self, text="SCTP", variable=self.__sctp_checked)

        self.__arp_checked = tk.BooleanVar()
        self.__arp_checked.set(True)
        arp_check = ttk.Checkbutton(self, text="ARP", variable=self.__arp_checked)

        tcp_check.grid(row=1, column=1)
        udp_check.grid(row=1, column=5)
        sctp_check.grid(row=1, column=9)
        arp_check.grid(row=1, column=13)

    @property
    def tcp_checked(self):
        return self.__tcp_checked

    @property
    def udp_checked(self):
        return self.__udp_checked

    @property
    def sctp_checked(self):
        return self.__sctp_checked

    @property
    def arp_checked(self):
        return self.__arp_checked
