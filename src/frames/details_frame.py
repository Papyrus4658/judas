import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import constants as c


class DetailsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.__fixedFont = tkFont.nametofont("TkFixedFont")
        self.__fixedFont.configure(size=c.FONT_SIZE)

        title = tk.Label(self, text=c.HEX_DUMP)
        self.__details = tk.Text(self, wrap=tk.NONE, font=self.__fixedFont)

        yscroll = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.__details.yview,
        )
        self.__details.configure(yscroll=yscroll.set)

        xscroll = ttk.Scrollbar(
            self, orient=tk.HORIZONTAL, command=self.__details.xview
        )
        self.__details.configure(xscroll=xscroll.set)

        title.grid(row=1, column=1)
        self.__details.grid(row=5, column=1, sticky="nsew")
        yscroll.grid(row=5, column=5, sticky="ns")
        xscroll.grid(row=9, column=1, sticky="ew")

    def delete_details(self):
        self.__details.delete("1.0", tk.END)

    def insert_details(self, details):
        self.__details.insert(tk.END, details)
