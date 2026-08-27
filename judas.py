import ipaddress
import queue
import sys
import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as mb
from datetime import datetime
from tkinter import ttk

from scapy.all import (
    ARP,
    IP,
    SCTP,
    TCP,
    UDP,
    AsyncSniffer,
    IPv6,
    hexdump,
    scapy,
)

import constants as c


class MainWin:
    def __init__(self):
        # キューとパケット保持用の辞書を追加
        self.packet_queue = queue.Queue()
        self.packet_store = {}

        # メインウィンドウを設定
        self.root = tk.Tk()
        max_width = self.root.winfo_screenwidth()
        max_height = self.root.winfo_screenheight()
        self.root.geometry(f"{max_width}x{max_height}")
        self.root.title("Judas")

        # フォントを設定
        proportional = tkfont.Font(family="BIZ_UDPGothic", size=c.FONT_SIZE)
        fixed_width = tkfont.Font(family="monospace", size=c.FONT_SIZE)

        # 設定フレームを設定
        config_frame = tk.Frame(self.root)

        # プルダウンメニューを設定
        interface_frame = tk.Frame(config_frame)

        interface_label = tk.Label(
            interface_frame, text=c.PROMPT_SELECT_INTERFACE, font=proportional
        )

        iface_names = self.get_ifaces()

        interface = ttk.Combobox(
            interface_frame,
            values=iface_names,
            state="readonly",
            font=proportional,
            # width=30,
        )
        interface.set(iface_names[0])

        # フィルターを設定
        filter_frame = tk.Frame(config_frame)

        # 初期値を設定
        self.tcp_checked = tk.BooleanVar()
        self.udp_checked = tk.BooleanVar()
        self.sctp_checked = tk.BooleanVar()
        self.arp_checked = tk.BooleanVar()

        self.tcp_checked.set(True)
        self.udp_checked.set(True)
        self.sctp_checked.set(True)
        self.arp_checked.set(False)

        tcp = tk.Checkbutton(
            filter_frame,
            text="TCP",
            variable=self.tcp_checked,
            font=proportional,
        )
        udp = tk.Checkbutton(
            filter_frame,
            text="UDP",
            variable=self.udp_checked,
            font=proportional,
        )
        sctp = tk.Checkbutton(
            filter_frame,
            text="SCTP",
            variable=self.sctp_checked,
            font=proportional,
        )
        arp = tk.Checkbutton(
            filter_frame,
            text="ARP",
            variable=self.arp_checked,
            font=proportional,
        )

        # ポート番号入力欄を設定
        port_frame = tk.Frame(config_frame)
        port_label = tk.Label(port_frame, text=c.PROMPT_INPUT_PORT, font=proportional)
        port = tk.Spinbox(
            port_frame,
            from_=0,
            to=65535,
            increment=1,
            font=fixed_width,
            textvariable=tk.IntVar(value=c.HTTPS_PORT),
        )

        # IPアドレス入力欄を設定
        ipaddress_frame = tk.Frame(config_frame)
        ipaddress_label = tk.Label(
            ipaddress_frame,
            text=c.PROMPT_INPUT_IP,
            font=proportional,
        )
        ip = tk.Entry(ipaddress_frame, font=fixed_width)

        # 自動スクロール選択ボタンを設定
        self.autoscroll_checked = tk.BooleanVar()
        self.autoscroll_checked.set(True)

        autoscroll = tk.Checkbutton(
            config_frame,
            variable=self.autoscroll_checked,
            text=c.SWITCH_AUTOSCROLL,
            font=proportional,
        )

        # 実行ボタンを設定
        buttons_frame = tk.Frame(self.root)
        start_button = tk.Button(
            buttons_frame,
            text=c.START,
            font=proportional,
            command=lambda: self.start_capture(
                start_button,
                stop_button,
                interface.get(),
                port.get(),
                ip.get(),
                captured_list,
            ),
        )
        stop_button = tk.Button(
            buttons_frame,
            text=c.STOP,
            font=proportional,
            command=lambda: self.stop_capture(start_button, stop_button),
        )
        delete_button = tk.Button(
            buttons_frame,
            text=c.DELETE,
            font=proportional,
            state=tk.DISABLED,
            command=lambda: self.delete_history(captured_list),
        )
        exit_button = tk.Button(
            buttons_frame,
            text=c.EXIT,
            font=proportional,
            command=lambda: self.exit_app(),
        )

        # パケット一覧表示欄を設定
        captured_list_frame = tk.Frame(self.root)
        captured_list_title = tk.Label(
            captured_list_frame,
            text=c.CAPTURED_LIST,
            font=proportional,
        )
        captured_list = ttk.Treeview(
            captured_list_frame,
            columns=c.COLS,
            height=15,
            show="headings",
        )

        for col in c.COLS:
            captured_list.heading(col, text=col)

        yscroll = ttk.Scrollbar(
            captured_list_frame,
            orient=tk.VERTICAL,
            command=captured_list.yview,
        )
        captured_list.configure(yscroll=yscroll.set)

        style = ttk.Style()
        style.configure("Treeview", font=fixed_width)
        style.configure("Treeview.Heading", font=proportional)

        # 16進ダンプ表示欄を設定
        hex_dump_frame = tk.Frame(self.root)
        hex_dump_title = tk.Label(hex_dump_frame, text=c.HEX_DUMP, font=proportional)
        hex_dump = tk.Text(hex_dump_frame, font=fixed_width)
        hex_dump.configure(font=fixed_width)

        # rootの1列目を伸縮可能に設定
        self.root.grid_columnconfigure(1, weight=1)

        # captured_list_frame内の列も伸縮可能に設定
        captured_list_frame.grid_columnconfigure(1, weight=1)

        # 16進ダンプも伸縮可能に設定
        hex_dump_frame.grid_columnconfigure(1, weight=1)

        # ウィンドウに配置
        config_frame.grid(row=1, column=1)
        buttons_frame.grid(row=1, column=5)
        captured_list_frame.grid(row=5, column=1, sticky="nsew", columnspan=5)
        hex_dump_frame.grid(row=9, column=1, sticky="nsew", columnspan=5)

        # 設定フレームに配置
        interface_frame.grid(row=1, column=1, rowspan=5)
        port_frame.grid(row=1, column=5, rowspan=5)
        ipaddress_frame.grid(row=1, column=9, rowspan=5)
        filter_frame.grid(row=1, column=13)
        autoscroll.grid(row=5, column=13)

        # ネットワークインターフェースフレームに配置
        interface_label.grid(row=1, column=1)
        interface.grid(row=5, column=1)

        # フィルターフレームに配置
        tcp.grid(row=1, column=1)
        udp.grid(row=1, column=5)
        sctp.grid(row=1, column=9)
        arp.grid(row=1, column=13)

        # ポート番号フレームに配置
        port_label.grid(row=1, column=1)
        port.grid(row=5, column=1)

        # IPアドレスフレームに配置
        ipaddress_label.grid(row=1, column=1)
        ip.grid(row=5, column=1)

        # ボタンフレームに配置
        start_button.grid(row=1, column=1)
        delete_button.grid(row=5, column=1)
        exit_button.grid(row=9, column=1)

        # パケット一覧フレームに配置
        captured_list_title.grid(row=1, column=1)
        captured_list.grid(row=5, column=1, sticky="nsew")
        yscroll.grid(row=5, column=5, sticky="ns")

        # 16進ダンプフレームに配置
        hex_dump_title.grid(row=1, column=1)
        hex_dump.grid(row=5, column=1, sticky="nsew")

    def get_ifaces(self):
        iface_names = list(scapy.interfaces.ifaces.data.keys())
        return iface_names

    def start_capture(
        self, start_button, stop_button, interface, port, ip, captured_list
    ):
        if interface == "":
            mb.showwarning(c.NOT_SNIFF, message=c.PROMPT_SELECT_INTERFACE)
            return

        input_filter = ""

        if ip != "":
            ip = ipaddress.ip_address(ip)
            print(type(ip))

            try:
                if isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
                    input_filter += "host " + ip
            except ValueError:
                mb.showwarning(
                    c.UNABLE_START,
                    message=c.IP_NOT_FORMATTED,
                )

        try:
            if port != "" and int(port) >= 0 and int(port) <= 65535:
                if input_filter != "":
                    input_filter += " and "

                input_filter += "port " + port
        except ValueError:
            mb.showwarning(c.UNABLE_START, message=c.PORT_NOT_INT)
            return

        self.sniffer = AsyncSniffer(
            iface=interface,
            filter=input_filter,
            prn=self.packet_callback,
            store=False,
        )

        self.sniffer.start()

        self.switch_buttons(start_button, stop_button)

    def packet_callback(self, pkt):
        if not self.protocol_checked(pkt):
            return

        now = datetime.now().strftime("%H:%M:%S.%f")
        print(pkt.summary())

    def protocol_checked(self, pkt):
        if pkt.haslayer(TCP):
            return self.tcp_checked.get()

        if pkt.haslayer(UDP):
            return self.udp_checked.get()

        if pkt.haslayer(SCTP):
            return self.sctp_checked.get()

        if pkt.haslayer(ARP):
            return self.arp_checked.get()

        return False

    def create_row(self):

        return

    def stop_capture(self, start_button, stop_button):
        if hasattr(self, "sniffer") and self.sniffer.running:
            self.sniffer.stop()

        self.switch_buttons(stop_button, start_button)

    def switch_buttons(self, enable, disable):
        enable.grid_forget()
        enable.configure(state=tk.DISABLED)

        disable.grid(row=1, column=1)
        disable.configure(state=tk.ACTIVE)

    def delete_history(self, captured_list):
        captured_list.delete()

    def exit_app(self):
        sys.exit(0)


def main():
    mw = MainWin()
    mw.root.mainloop()


if __name__ == "__main__":
    main()
