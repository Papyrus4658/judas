import ipaddress
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
        port_label = tk.Label(
            port_frame,
            text=c.PROMPT_INPUT_PORT,
            font=proportional,
        )
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
            ),
        )
        stop_button = tk.Button(
            buttons_frame,
            text=c.STOP,
            font=proportional,
            command=lambda: self.stop_capture(start_button, stop_button),
        )
        self.delete_button = tk.Button(
            buttons_frame,
            text=c.DELETE,
            font=proportional,
            state=tk.DISABLED,
            command=lambda: self.delete_record(),
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
        self.captured_list = ttk.Treeview(
            captured_list_frame,
            columns=c.COLS,
            height=15,
            show="headings",
        )
        self.captured_list.bind("<<TreeviewSelect>>", self.display_hex_dump)

        for col in c.COLS:
            self.captured_list.heading(col, text=col)

        list_yscroll = ttk.Scrollbar(
            captured_list_frame,
            orient=tk.VERTICAL,
            command=self.captured_list.yview,
        )
        self.captured_list.configure(yscroll=list_yscroll.set)

        style = ttk.Style()
        style.configure("Treeview", font=fixed_width, rowheight=25)
        style.configure("Treeview.Heading", font=proportional)

        # 16進ダンプ表示欄を設定
        hex_dump_frame = tk.Frame(self.root)
        hex_dump_title = tk.Label(
            hex_dump_frame,
            text=c.HEX_DUMP,
            font=proportional,
        )
        self.hex_dump = tk.Text(hex_dump_frame, font=fixed_width, wrap=tk.NONE)

        details_yscroll = ttk.Scrollbar(
            hex_dump_frame,
            orient=tk.VERTICAL,
            command=self.hex_dump.yview,
        )
        self.hex_dump.configure(yscroll=details_yscroll.set)

        details_xscroll = ttk.Scrollbar(
            hex_dump_frame,
            orient=tk.HORIZONTAL,
            command=self.hex_dump.xview,
        )
        self.hex_dump.configure(xscroll=details_xscroll.set)

        # rootの1列目を伸縮可能に設定
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(5, weight=1)  # パケット一覧の列
        self.root.grid_rowconfigure(9, weight=1)  # 16進ダンプの列

        # パケット一覧の列も伸縮可能に設定
        captured_list_frame.grid_columnconfigure(1, weight=1)
        captured_list_frame.grid_rowconfigure(5, weight=1)

        # 16進ダンプも伸縮可能に設定
        hex_dump_frame.grid_columnconfigure(1, weight=1)
        hex_dump_frame.grid_rowconfigure(5, weight=1)

        # ウィンドウに配置
        config_frame.grid(row=1, column=1)
        buttons_frame.grid(row=1, column=5)
        captured_list_frame.grid(
            row=5,
            column=1,
            sticky="nsew",
            columnspan=5,
        )
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
        self.delete_button.grid(row=5, column=1)
        exit_button.grid(row=9, column=1)

        # パケット一覧フレームに配置
        captured_list_title.grid(row=1, column=1)
        self.captured_list.grid(row=5, column=1, sticky="nsew")
        list_yscroll.grid(row=5, column=5, sticky="ns")

        # 16進ダンプフレームに配置
        hex_dump_title.grid(row=1, column=1)
        self.hex_dump.grid(row=5, column=1, sticky="nsew")
        details_yscroll.grid(row=5, column=5, sticky="ns")
        details_xscroll.grid(row=9, column=1, sticky="ew")

    def get_ifaces(self):
        iface_names = list(scapy.interfaces.ifaces.data.keys())
        return iface_names

    def start_capture(
        self,
        start_button,
        stop_button,
        interface,
        port,
        ip,
    ) -> None:
        if interface == "":
            mb.showwarning(c.NOT_SNIFF, message=c.PROMPT_SELECT_INTERFACE)
            return

        input_filter = ""

        if ip != "":
            try:
                parsed_ip = ipaddress.ip_address(ip)

                if isinstance(
                    parsed_ip,
                    (
                        ipaddress.IPv4Address,
                        ipaddress.IPv6Address,
                    ),
                ):
                    input_filter += "host " + parsed_ip
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

    def packet_callback(self, pkt) -> None:
        if not self.protocol_checked(pkt):
            return

        self.create_row(pkt)

    def protocol_checked(self, pkt) -> bool:
        if pkt.haslayer(TCP):
            return self.tcp_checked.get()

        if pkt.haslayer(UDP):
            return self.udp_checked.get()

        if pkt.haslayer(SCTP):
            return self.sctp_checked.get()

        if pkt.haslayer(ARP):
            return self.arp_checked.get()

        return False

    def create_row(self, pkt):
        now = datetime.now().strftime("%H:%M:%S.%f")
        size = len(pkt)

        if pkt.haslayer(TCP):
            protocol = "TCP"
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            flags = str(pkt[TCP].flags)
        elif pkt.haslayer(UDP):
            protocol = "UDP"
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport
            flags = ""
        elif pkt.haslayer(SCTP):
            protocol = "SCTP"
            sport = pkt[SCTP].sport
            dport = pkt[SCTP].dport
            flags = ""
        elif pkt.haslayer(ARP):
            protocol = "ARP"
            sport = pkt[ARP].sport
            dport = pkt[ARP].dport
            flags = f"op={pkt[ARP].op}"
        else:
            return

        if pkt.haslayer(IP):
            src = pkt[IP].src
            dst = pkt[IP].dst
        elif pkt.haslayer(IPv6):
            src = pkt[IPv6].src
            dst = pkt[IPv6].dst
        else:
            return

        iid = self.captured_list.insert(
            parent="",
            index="end",
            values=(now, protocol, src, sport, dst, dport, flags, size),
        )

        if self.autoscroll_checked.get():
            self.captured_list.yview_moveto(1.0)

        # 消去ボタンを押せるようにする
        if self.delete_button["state"] == tk.DISABLED:
            self.delete_button.configure(state=tk.ACTIVE)

        self.packet_store[iid] = pkt

    def stop_capture(self, start_button, stop_button) -> None:
        if hasattr(self, "sniffer") and self.sniffer.running:
            self.sniffer.stop()

        self.switch_buttons(stop_button, start_button)

    def switch_buttons(self, enable, disable) -> None:
        enable.grid_forget()
        enable.configure(state=tk.DISABLED)

        disable.grid(row=1, column=1)
        disable.configure(state=tk.ACTIVE)

    def display_hex_dump(self, event) -> None:
        record = self.captured_list.selection()  # 選択した列のidを取得

        if not record:
            return

        pkt = self.packet_store[record[0]]  # idからパケットを取得

        details = (  # パケットのレイヤー構造と16進ダンプを結合
            "===Packet Structure===\n"
            + pkt.show(dump=True)
            + "\n===Hex Dump===\n"
            + hexdump(pkt, dump=True)
        )

        self.hex_dump.delete("1.0", tk.END)  # 既存の内容を削除
        self.hex_dump.insert(tk.END, details)  # 詳細を書き込み

    def delete_record(self) -> None:
        self.captured_list.delete(*self.captured_list.get_children())
        self.packet_store.clear()
        self.hex_dump.delete("1.0", tk.END)
        self.delete_button.configure(state=tk.DISABLED)

    def exit_app(self) -> None:
        sys.exit(0)


def main():
    mw = MainWin()
    mw.root.mainloop()


if __name__ == "__main__":
    main()
