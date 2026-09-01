import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk

import constants as c


class DetailsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        fixed_font = tk_font.nametofont("TkFixedFont")
        fixed_font.configure(size=c.FONT_SIZE)

        title = ttk.Label(self, text=c.HEX_DUMP)
        self._details = tk.Text(self, wrap=tk.NONE, font=fixed_font)

        yscroll = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self._details.yview,
        )
        self._details.configure(yscroll=yscroll.set)

        xscroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._details.xview)
        self._details.configure(xscroll=xscroll.set)

        title.grid(row=1, column=1)
        self._details.grid(row=5, column=1, sticky="nsew")
        yscroll.grid(row=5, column=5, sticky="ns")
        xscroll.grid(row=9, column=1, sticky="ew")

    def delete_details(self):
        self._details.delete("1.0", tk.END)

    def insert_details(self, details):
        self._details.insert(tk.END, details)
