import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk

import constants as c


class RecordsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        default_font = tk_font.nametofont("TkDefaultFont")
        default_font.configure(size=c.FONT_SIZE)

        title = ttk.Label(self, text=c.CAPTURED_LIST)
        self._records = ttk.Treeview(
            self,
            columns=c.COLS,
            height=20,
            show="headings",
        )

        for col in c.COLS:
            self._records.heading(col, text=col)

        yscroll = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self._records.yview,
        )
        self._records.configure(yscroll=yscroll.set)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=default_font)

        title.grid(row=1, column=1)
        self._records.grid(row=5, column=1, sticky="nsew")
        yscroll.grid(row=5, column=5, sticky="ns")

    @property
    def records(self):
        return self._records

    def insert_record(self, parent, index, record):
        return self._records.insert(parent, index, values=record)

    def y_scroll(self):
        self._records.yview_moveto(1.0)

    def get_selected(self):
        return self._records.selection()

    def delete_records(self):
        self._records.delete(*self._records.get_children())
