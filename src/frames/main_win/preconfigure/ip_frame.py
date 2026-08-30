from tkinter import ttk

import constants as c


class IpFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        ipaddress_label = ttk.Label(self, text=c.PROMPT_INPUT_IP)
        self.__ip_entry = ttk.Entry(self)

        ipaddress_label.grid(row=1, column=1)
        self.ip_entry.grid(row=5, column=1)

    @property
    def ip_entry(self):
        return self.__ip_entry
