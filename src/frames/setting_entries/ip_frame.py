import tkinter.font as tk_font
from tkinter import ttk

import constants as c


class IpFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        fixed_font = tk_font.nametofont("TkFixedFont")
        fixed_font.configure(size=c.FONT_SIZE)

        title = ttk.Label(self, text=c.PROMPT_INPUT_IP)
        self._entry = ttk.Entry(self, font=fixed_font)

        title.grid(row=1, column=1)
        self._entry.grid(row=5, column=1)

    @property
    def entry(self):
        return self._entry
