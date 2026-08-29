import tkinter as tk
from tkinter import ttk

import constants as c
import filters_frame as ff
import ip_frame as ipf
import port_frame as pof
import select_iface_frame as sif


class PreconfigureFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # プルダウンメニューを設定
        self.__select_iface_frame = sif.SelectIfaceFrame(self)

        # ポート番号入力欄を設定
        self.__port_frame = pof.PortFrame(self)

        # IPアドレス入力欄を設定
        self.__ip_frame = ipf.IpFrame(self)

        # フィルターを設定
        self.__filters_frame = ff.FiltersFrame(self)

        # 自動スクロール選択ボタンを設定
        self.autoscroll_checked = tk.BooleanVar()
        self.autoscroll_checked.set(True)

        autoscroll = ttk.Checkbutton(
            self,
            variable=self.autoscroll_checked,
            text=c.SWITCH_AUTOSCROLL,
        )

        self.__select_iface_frame.grid(row=1, column=1, rowspan=5)
        self.__port_frame.grid(row=1, column=5, rowspan=5)
        self.__ip_frame.grid(row=1, column=9, rowspan=5)
        self.__filters_frame.grid(row=1, column=13)
        autoscroll.grid(row=5, column=13)

    @property
    def select_iface_frame(self):
        return self.__select_iface_frame

    @property
    def port_frame(self):
        return self.__port_frame

    @property
    def ip_frame(self):
        return self.__ip_frame

    @property
    def filters_frame(self):
        return self.__filters_frame
