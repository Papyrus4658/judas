import ipaddress
import queue
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as mb
from datetime import datetime

from scapy.all import ARP, IP, SCTP, TCP, UDP, AsyncSniffer, IPv6, hexdump

import constants as c
import frames.main_win.buttons_frame as bf
import frames.main_win.captured_records_frame as crf
import frames.main_win.details_frame as df
import frames.main_win.preconfigure_frame as prf


class MainWin:
    def __init__(self):
        self.q = queue.Queue()
        self.packet_store = {}

        self.root = tk.Tk()
        max_width = self.root.winfo_screenwidth()
        max_height = self.root.winfo_screenheight()
        self.root.geometry(f"{max_width}x{max_height}")
        self.root.title("Judas")

        __defaultFont = tkFont.nametofont("TkDefaultFont")
        __defaultFont.configure(size=c.FONT_SIZE)

        self.__preconfigure_frame = prf.PreconfigureFrame(self.root)

        self.__buttons_frame = bf.ButtonsFrame(self.root)
        self.__buttons_frame.start_button.configure(
            command=lambda: self.start_capture(
                self.__buttons_frame.start_button,
                self.__buttons_frame.stop_button,
                self.__preconfigure_frame.select_iface_frame.ifaces_combo.get(),
                self.__preconfigure_frame.port_frame.port_spin.get(),
                self.__preconfigure_frame.ip_frame.ip_entry.get(),
            ),
        )
        self.__buttons_frame.stop_button.configure(
            command=lambda: self.stop_capture(
                self.__buttons_frame.start_button, self.__buttons_frame.stop_button
            )
        )
        self.__buttons_frame.delete_button.configure(
            command=lambda: self.delete_record()
        )

        self.__captured_records_frame = crf.CapturedRecordsFrame(self.root)
        self.__captured_records_frame.captured_records.bind(
            "<<TreeviewSelect>>", self.display_details
        )

        self.__details_frame = df.DetailsFrame(self.root)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(9, weight=1)

        self.__captured_records_frame.grid_columnconfigure(1, weight=1)
        self.__captured_records_frame.grid_rowconfigure(5, weight=1)

        self.__details_frame.grid_columnconfigure(1, weight=1)
        self.__details_frame.grid_rowconfigure(5, weight=1)

        self.__preconfigure_frame.grid(row=1, column=1)
        self.__buttons_frame.grid(row=1, column=5)
        self.__captured_records_frame.grid(row=5, column=1, sticky="nsew", columnspan=5)
        self.__details_frame.grid(row=9, column=1, sticky="nsew", columnspan=5)

    @property
    def preconfigure_frame(self):
        return self.__preconfigure_frame

    @property
    def buttons_frame(self):
        return self.__buttons_frame

    @property
    def captured_records_frame(self):
        return self.__captured_records_frame

    @property
    def details_frame(self):
        return self.__details_frame

    def start_capture(self, start_button, stop_button, interface, port, ip):
        if interface == "":
            mb.showwarning(c.NOT_SNIFF, message=c.PROMPT_SELECT_INTERFACE)
            return

        input_filter = ""

        if ip != "":
            try:
                parsed_ip = ipaddress.ip_address(ip)
                if isinstance(
                    parsed_ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)
                ):
                    input_filter += "host " + str(parsed_ip)
            except ValueError:
                mb.showwarning(c.UNABLE_START, message=c.IP_NOT_FORMATTED)
                return

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

        self.__buttons_frame.switch_buttons(start_button, stop_button)

    def stop_capture(self, start_button, stop_button):
        if hasattr(self, "sniffer") and self.sniffer.running:
            self.sniffer.stop()
            self.__buttons_frame.switch_buttons(stop_button, start_button)

    def packet_callback(self, pkt):
        if not self.protocol_checked(pkt):
            return

        self.create_record(pkt)

    def protocol_checked(self, pkt) -> bool:
        if pkt.haslayer(TCP):
            return self.__preconfigure_frame.filters_frame.tcp_checked.get()

        if pkt.haslayer(UDP):
            return self.__preconfigure_frame.filters_frame.udp_checked.get()

        if pkt.haslayer(SCTP):
            return self.__preconfigure_frame.filters_frame.sctp_checked.get()

        if pkt.haslayer(ARP):
            return self.__preconfigure_frame.filters_frame.arp_checked.get()

        return False

    def create_record(self, pkt):
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

        now = datetime.now(c.LOCAL_TZ).time().strftime(c.TIME_FORMAT)
        record = (now, protocol, src, sport, dst, dport, flags, size)
        iid = self.__captured_records_frame.captured_records.insert(
            "", "end", values=record
        )
        self.packet_store[iid] = pkt

        if self.__preconfigure_frame.autoscroll_checked.get():
            self.__captured_records_frame.captured_records.yview_moveto(1.0)

        self.__buttons_frame.delete_button.configure(state=tk.ACTIVE)

    def display_details(self, event):
        record = self.__captured_records_frame.captured_records.selection()

        if not record:
            return

        pkt = self.packet_store[record[0]]
        packet_structure = c.PACKET_STRUCTURE_HEAD + pkt.show(dump=True)
        hex_dump = c.HEX_DUMP_HEAD + hexdump(pkt, dump=True)
        details = packet_structure + hex_dump

        self.__details_frame.details.delete("1.0", tk.END)
        self.__details_frame.details.insert(tk.END, details)

    def delete_record(self):
        self.__captured_records_frame.captured_records.delete(
            *self.__captured_records_frame.captured_records.get_children()
        )
        self.packet_store.clear()
        self.__details_frame.details.delete("1.0", tk.END)
        self.__buttons_frame.delete_button.configure(state=tk.DISABLED)


def main():
    mw = MainWin()
    mw.root.mainloop()


if __name__ == "__main__":
    main()
