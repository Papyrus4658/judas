import tkinter as tk
from tkinter import ttk

import constants as c


class DetailsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        details_title = tk.Label(self, text=c.HEX_DUMP)
        self.__details = tk.Text(self, wrap=tk.NONE)

        details_yscroll = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.details.yview
        )
        self.details.configure(yscroll=details_yscroll.set)

        details_xscroll = ttk.Scrollbar(
            self, orient=tk.HORIZONTAL, command=self.details.xview
        )
        self.details.configure(xscroll=details_xscroll.set)

        details_title.grid(row=1, column=1)
        self.details.grid(row=5, column=1, sticky="nsew")
        details_yscroll.grid(row=5, column=5, sticky="ns")
        details_xscroll.grid(row=9, column=1, sticky="ew")

    @property
    def details(self):
        return self.__details
