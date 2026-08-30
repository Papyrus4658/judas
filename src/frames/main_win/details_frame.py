import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import constants as c


class DetailsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.__fixedFont = tkFont.nametofont("TkFixedFont")
        self.__fixedFont.configure(size=c.FONT_SIZE)

        details_title = tk.Label(self, text=c.HEX_DUMP)
        self.__details = tk.Text(self, wrap=tk.NONE, font=self.__fixedFont)

        details_yscroll = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.__details.yview
        )
        self.__details.configure(yscroll=details_yscroll.set)

        details_xscroll = ttk.Scrollbar(
            self, orient=tk.HORIZONTAL, command=self.__details.xview
        )
        self.__details.configure(xscroll=details_xscroll.set)

        details_title.grid(row=1, column=1)
        self.__details.grid(row=5, column=1, sticky="nsew")
        details_yscroll.grid(row=5, column=5, sticky="ns")
        details_xscroll.grid(row=9, column=1, sticky="ew")

    @property
    def details(self):
        return self.__details
