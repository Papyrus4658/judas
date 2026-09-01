import sys
import tkinter as tk
from tkinter import ttk

import constants as c


class ButtonsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self._start_button = ttk.Button(self, text=c.START)
        self._stop_button = ttk.Button(self, text=c.STOP)
        self._del_button = ttk.Button(self, text=c.DELETE, state=tk.DISABLED)
        self._exit_button = ttk.Button(
            self, text=c.EXIT, command=lambda: self.exit_app()
        )

        self._start_button.grid(row=1, column=1)
        self._del_button.grid(row=5, column=1)
        self._exit_button.grid(row=9, column=1)

    @property
    def start_button(self):
        return self._start_button

    @property
    def stop_button(self):
        return self._stop_button

    @property
    def del_button(self):
        return self._del_button

    def switch_buttons(self, hide, show):
        hide.grid_forget()
        hide.configure(state=tk.DISABLED)

        show.grid(row=1, column=1)
        show.configure(state=tk.NORMAL)

    def exit_app(self):
        sys.exit(0)

    def normalize_delete_button(self):
        self._del_button.configure(state=tk.NORMAL)

    def disable_delete_button(self):
        self._del_button.configure(state=tk.DISABLED)
