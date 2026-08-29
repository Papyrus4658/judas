import tkinter as tk
from tkinter import ttk

import constants as c


class CapturedRecordsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        captured_records_title = ttk.Label(
            self,
            text=c.CAPTURED_LIST,
        )
        self.__captured_records = ttk.Treeview(
            self,
            columns=c.COLS,
            height=15,
            show="headings",
        )

        for col in c.COLS:
            self.__captured_records.heading(col, text=col)

        list_yscroll = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.__captured_records.yview,
        )
        self.__captured_records.configure(yscroll=list_yscroll.set)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading")

        # パケット一覧フレームに配置
        captured_records_title.grid(row=1, column=1)
        self.__captured_records.grid(row=5, column=1, sticky="nsew")
        list_yscroll.grid(row=5, column=5, sticky="ns")

    @property
    def captured_records(self):
        return self.__captured_records
