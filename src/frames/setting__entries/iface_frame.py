import tkinter.font as tkFont
from tkinter import ttk

from scapy.all import scapy

import constants as c


class IfaceFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        title = ttk.Label(self, text=c.PROMPT_SELECT_IFACE)

        self.__defaultFont = tkFont.nametofont("TkDefaultFont")
        self.__defaultFont.configure(size=c.FONT_SIZE)

        iface_names = self.get_ifaces()
        self.__combo = ttk.Combobox(
            self,
            values=iface_names,
            state="readonly",
            font=self.__defaultFont,
        )
        self.__combo.set(iface_names[0])

        title.grid(row=1, column=1)
        self.__combo.grid(row=5, column=1)

    @property
    def combo(self):
        return self.__combo

    def get_ifaces(self):
        iface_names = list(scapy.interfaces.ifaces.data.keys())
        return iface_names
