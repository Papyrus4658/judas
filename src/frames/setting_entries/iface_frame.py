import tkinter.font as tk_font
from tkinter import ttk

import scapy

import constants as c


class IfaceFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        title = ttk.Label(self, text=c.PROMPT_SELECT_IFACE)

        default_font = tk_font.nametofont("TkDefaultFont")
        default_font.configure(size=c.FONT_SIZE)

        iface_names = self.get_ifaces()
        self._combo = ttk.Combobox(
            self,
            values=iface_names,
            state="readonly",
            font=default_font,
        )
        self._combo.set(iface_names[0])

        title.grid(row=1, column=1)
        self._combo.grid(row=5, column=1)

    @property
    def combo(self):
        return self._combo

    def get_ifaces(self):
        iface_names = list(scapy.interfaces.get_if_list())
        return iface_names
