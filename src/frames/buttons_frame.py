import sys
import tkinter as tk
from tkinter import ttk

import constants as c


class ButtonsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.__start_button = ttk.Button(self, text=c.START)
        self.__stop_button = ttk.Button(self, text=c.STOP)
        self.__del_button = ttk.Button(self, text=c.DELETE, state=tk.DISABLED)
        self.__exit_button = ttk.Button(
            self, text=c.EXIT, command=lambda: self.exit_app()
        )

        self.__start_button.grid(row=1, column=1)
        self.__del_button.grid(row=5, column=1)
        self.__exit_button.grid(row=9, column=1)

    @property
    def start_button(self):
        return self.__start_button

    @property
    def stop_button(self):
        return self.__stop_button

    @property
    def del_button(self):
        return self.__del_button

    def switch_buttons(self, normal, disable):
        normal.grid_forget()
        normal.configure(state=tk.DISABLED)

        disable.grid(row=1, column=1)
        disable.configure(state=tk.NORMAL)

    def exit_app(self):
        sys.exit(0)

    def normalize_delete_button(self):
        self.__del_button.configure(state=tk.NORMAL)

    def disable_delete_button(self):
        self.__del_button.configure(state=tk.DISABLED)
