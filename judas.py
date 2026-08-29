import ipaddress
import sys
import tkinter as tk
import tkinter.messagebox as mb
from datetime import datetime

from scapy.all import (
    ARP,
    IP,
    SCTP,
    TCP,
    UDP,
    AsyncSniffer,
    IPv6,
    hexdump,
)

import buttons_frame as bf
import captured_records_frame as crf
import constants as c
import details_frame as df
import preconfigure_frame as prf


class MainWin:
    def __init__(self):
        self.packet_store = {}

        # メインウィンドウを設定
        self.root = tk.Tk()
        max_width = self.root.winfo_screenwidth()
        max_height = self.root.winfo_screenheight()
        self.root.geometry(f"{max_width}x{max_height}")
        self.root.title("Judas")

        # 設定フレームを設定
        self.__preconfigure_frame = prf.PreconfigureFrame(self.root)

        # 実行ボタンを設定
        buttons_frame = bf.ButtonsFrame(self.root)

        buttons_frame.start_button.configure(
            command=lambda: self.start_capture(
                buttons_frame.start_button,
                buttons_frame.stop_button,
                self.__preconfigure_frame.select_iface_frame.ifaces_combo.get(),
                self.__preconfigure_frame.port_frame.port_spin.get(),
                self.__preconfigure_frame.ip_frame.ip_entry.get(),
            ),
        )

        buttons_frame.stop_button.configure(
            command=lambda: self.stop_capture(
                buttons_frame.start_button, buttons_frame.stop_button
            )
        )

        buttons_frame.delete_button.configure(command=lambda: self.delete_record())

        buttons_frame.exit_button.configure(command=lambda: self.exit_app())

        # パケット一覧表示欄を設定
        captured_records_frame = crf.CapturedRecordsFrame(self.root)

        captured_records_frame.captured_records.bind(
            "<<TreeviewSelect>>", self.display_hex_dump
        )

        # 16進ダンプ表示欄を設定
        details_frame = df.DetailsFrame(self.root)

        # rootの1列目を伸縮可能に設定
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(5, weight=1)  # パケット一覧の列
        self.root.grid_rowconfigure(9, weight=1)  # 16進ダンプの列

        # パケット一覧の列も伸縮可能に設定
        captured_records_frame.grid_columnconfigure(1, weight=1)
        captured_records_frame.grid_rowconfigure(5, weight=1)

        # 16進ダンプも伸縮可能に設定
        details_frame.grid_columnconfigure(1, weight=1)
        details_frame.grid_rowconfigure(5, weight=1)

        # ウィンドウに配置
        self.__preconfigure_frame.grid(row=1, column=1)
        buttons_frame.grid(row=1, column=5)
        captured_records_frame.grid(
            row=5,
            column=1,
            sticky="nsew",
            columnspan=5,
        )
        details_frame.grid(row=9, column=1, sticky="nsew", columnspan=5)

    def preconfigure_frame(self):
        return self.__preconfigure_frame

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
            return self.preconfigure_frame.filters_frame.tcp_checked.get()

        if pkt.haslayer(UDP):
            return self.preconfigure_frame.filters_frame.udp_checked.get()

        if pkt.haslayer(SCTP):
            return self.preconfigure_frame.filters_frame.sctp_checked.get()

        if pkt.haslayer(ARP):
            return self.preconfigure_frame.filters_frame.arp_checked.get()

        return False

    def create_row(self, pkt):
        now = datetime.date().strftime("%H:%M:%S.%f")

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
