import tkinter as tk
from tkinter import ttk

import constants as c


class ButtonsFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.__start_button = ttk.Button(self, text=c.START)

        self.__stop_button = ttk.Button(self, text=c.STOP)

        self.__delete_button = ttk.Button(self, text=c.DELETE, state=tk.DISABLED)

        self.__exit_button = ttk.Button(self, text=c.EXIT)

        self.__start_button.grid(row=1, column=1)
        self.__delete_button.grid(row=5, column=1)
        self.__exit_button.grid(row=9, column=1)

    @property
    def start_button(self):
        return self.__start_button

    @property
    def stop_button(self):
        return self.__stop_button

    @property
    def delete_button(self):
        return self.__delete_button

    @property
    def exit_button(self):
        return self.__exit_button
