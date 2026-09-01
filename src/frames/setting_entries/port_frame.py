import tkinter.font as tk_font
from tkinter import ttk

import constants as c


class PortFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        fixed_font = tk_font.nametofont("TkFixedFont")
        fixed_font.configure(size=c.FONT_SIZE)

        title = ttk.Label(self, text=c.PROMPT_INPUT_PORT)

        self._spin = ttk.Spinbox(self, from_=0, to=65535, increment=1, font=fixed_font)
        self._spin.set(c.HTTPS_PORT)

        style = ttk.Style()
        style.configure("TSpinbox", arrowsize=c.FONT_SIZE)

        title.grid(row=1, column=1)
        self._spin.grid(row=5, column=1)

    @property
    def spin(self):
        return self._spin
