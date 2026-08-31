import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import constants as c


class RecordsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.__defaultFont = tkFont.nametofont("TkDefaultFont")
        self.__defaultFont.configure(size=c.FONT_SIZE)

        title = ttk.Label(self, text=c.CAPTURED_LIST)
        self.__records = ttk.Treeview(
            self,
            columns=c.COLS,
            height=20,
            show="headings",
        )

        for col in c.COLS:
            self.__records.heading(col, text=col)

        yscroll = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.__records.yview,
        )
        self.__records.configure(yscroll=yscroll.set)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=self.__defaultFont)

        title.grid(row=1, column=1)
        self.__records.grid(row=5, column=1, sticky="nsew")
        yscroll.grid(row=5, column=5, sticky="ns")

    @property
    def records(self):
        return self.__records

    def insert_record(self, parent, index, record):
        return self.__records.insert(parent, index, values=record)

    def y_scroll(self, fraction):
        self.__records.yview_moveto(1.0)

    def get_selected(self):
        return self.__records.selection()

    def delete_records(self):
        self.__records.delete(*self.__records.get_children())
