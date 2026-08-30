import tkinter.font as tkFont
from tkinter import ttk

from scapy.all import scapy

import constants as c


class SelectIfaceFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        select_iface_label = ttk.Label(self, text=c.PROMPT_SELECT_INTERFACE)

        self.__defaultFont = tkFont.nametofont("TkDefaultFont")
        self.__defaultFont.configure(size=c.FONT_SIZE)

        iface_names = self.get_ifaces()
        self.__ifaces_combo = ttk.Combobox(
            self, values=iface_names, state="readonly", font=self.__defaultFont
        )
        self.__ifaces_combo.set(iface_names[0])

        select_iface_label.grid(row=1, column=1)
        self.__ifaces_combo.grid(row=5, column=1)

    @property
    def ifaces_combo(self):
        return self.__ifaces_combo

    def get_ifaces(self):
        iface_names = list(scapy.interfaces.ifaces.data.keys())
        return iface_names
