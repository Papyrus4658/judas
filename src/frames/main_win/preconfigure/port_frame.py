from tkinter import ttk

import constants as c


class PortFrame(ttk.Frame):
    def __init__(self, preconfigure):
        super().__init__(preconfigure)

        port_label = ttk.Label(self, text=c.PROMPT_INPUT_PORT)

        self.__port_spin = ttk.Spinbox(self, from_=0, to=65535, increment=1)
        self.port_spin.set(c.HTTPS_PORT)

        port_label.grid(row=1, column=1)
        self.port_spin.grid(row=5, column=1)

    @property
    def port_spin(self):
        return self.__port_spin
