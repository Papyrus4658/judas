import ipaddress
import queue
import tkinter as tk
import tkinter.font as tk_font
import tkinter.messagebox as mb
from datetime import datetime

from scapy.all import ARP, IP, SCTP, TCP, UDP, AsyncSniffer, IPv6, hexdump

import capture
import constants as c
import frames.buttons_frame as buttons_f
import frames.details_frame as details_f
import frames.records_frame as records_f
import frames.settings_frame as settings_f


class MainWin:
    def __init__(self):
        self.q = queue.Queue()
        self.packet_store = {}
        self.cap = capture.Capture()

        self.root = tk.Tk()
        max_width = self.root.winfo_screenwidth()
        max_height = self.root.winfo_screenheight()
        self.root.geometry(f"{max_width}x{max_height}")
        self.root.title("Judas")

        default_font = tk_font.nametofont("TkDefaultFont")
        default_font.configure(size=c.FONT_SIZE)

        self._settings_frame = settings_f.SettingsFrame(self.root)

        self._buttons_frame = buttons_f.ButtonsFrame(self.root)
        self._buttons_frame.start_button.configure(
            command=lambda: self.start_capture(
                self._buttons_frame.start_button,
                self._buttons_frame.stop_button,
                self._settings_frame.get_iface(),
                self._settings_frame.get_port(),
                self._settings_frame.get_ip(),
            ),
        )
        self._buttons_frame.stop_button.configure(
            command=lambda: self.stop_capture(
                self._buttons_frame.start_button,
                self._buttons_frame.stop_button,
            )
        )
        self._buttons_frame.del_button.configure(
            command=lambda: self.delete_history(),
        )

        self._records_frame = records_f.RecordsFrame(self.root)
        self._records_frame.records.bind(
            "<<TreeviewSelect>>",
            self.display_details,
        )

        self._details_frame = details_f.DetailsFrame(self.root)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(9, weight=1)

        self._records_frame.grid_columnconfigure(1, weight=1)
        self._records_frame.grid_rowconfigure(5, weight=1)

        self._details_frame.grid_columnconfigure(1, weight=1)
        self._details_frame.grid_rowconfigure(5, weight=1)

        self._settings_frame.grid(row=1, column=1)
        self._buttons_frame.grid(row=1, column=5)
        self._records_frame.grid(
            row=5,
            column=1,
            sticky="nsew",
            columnspan=5,
        )
        self._details_frame.grid(
            row=9,
            column=1,
            sticky="nsew",
            columnspan=5,
        )

    def start_capture(self, start_button, stop_button, interface, port, ip):
        if interface == "":
            mb.showwarning(c.UNABLE_START, message=c.PROMPT_SELECT_IFACE)
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

        self._buttons_frame.switch_buttons(start_button, stop_button)

    def stop_capture(self, start_button, stop_button):
        if hasattr(self, "sniffer") and self.sniffer.running:
            self.sniffer.stop()
            self._buttons_frame.switch_buttons(stop_button, start_button)

    def packet_callback(self, pkt):
        if not self._settings_frame.check_protocol(pkt):
            return

        self.keep_capturing(pkt)

    def keep_capturing(self, pkt):
        record = self.cap.create_record(pkt)

        iid = self._records_frame.insert_record("", "end", record)

        self.packet_store[iid] = pkt

        if self._settings_frame.get_autoscroll():
            self._records_frame.y_scroll()

        self._buttons_frame.normalize_delete_button()

    def display_details(self, event):
        record = self._records_frame.get_selected()
        if not record:
            return

        pkt = self.packet_store[record[0]]
        packet_structure = c.PACKET_STRUCTURE + pkt.show(dump=True)
        hex_dump = c.HEX_DUMP_HEAD + hexdump(pkt, dump=True)
        details = packet_structure + hex_dump

        self._details_frame.delete_details()
        self._details_frame.insert_details(details)

    def delete_history(self):
        self.packet_store.clear()
        self._records_frame.delete_records()
        self._details_frame.delete_details()
        self._buttons_frame.disable_delete_button()


def main():
    mw = MainWin()
    mw.root.mainloop()


if __name__ == "__main__":
    main()
