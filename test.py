# from scapy.all import scapy

# ifaces = scapy.interfaces.ifaces.__dict__

# iface_data = ifaces.get("data")
# print(iface_data)
# # print(type(iface_data))

# for k in iface_data:
#     print(k)
#     print(type(k))

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

FONT_SIZE = 16

# メインウィンドウを設定
root = tk.Tk()
max_width = root.winfo_screenwidth()
max_height = root.winfo_screenheight()
root.geometry(f"{max_width}x{max_height}")
root.title("Judas")

# フォントを設定
proportional = tkfont.Font(family="BIZ_UDPGothic", size=FONT_SIZE)
fixed_width = tkfont.Font(family="monospace", size=FONT_SIZE)

# 設定フレームを設定
config_frame = tk.Frame(root)

# プルダウンメニューを設定
combo = ttk.Combobox(
    config_frame,
    values=["オムライス", "パンケーキ", "おまじないパフェ"],
    state="readonly",
    font=proportional,
    width=60,
)
combo.set("ネットワークインターフェースを選択")

# フィルターを設定
filter_frame = tk.Frame(config_frame)

# 初期値を設定
tcp_checked = tk.BooleanVar()
udp_checked = tk.BooleanVar()
sctp_checked = tk.BooleanVar()
arp_checked = tk.BooleanVar()

tcp_checked.set(True)
udp_checked.set(True)
sctp_checked.set(True)
arp_checked.set(False)

tcp = tk.Checkbutton(
    filter_frame,
    text="TCP",
    variable=tcp_checked,
    font=proportional,
)
udp = tk.Checkbutton(
    filter_frame,
    text="UDP",
    variable=udp_checked,
    font=proportional,
)
sctp = tk.Checkbutton(
    filter_frame,
    text="SCTP",
    variable=sctp_checked,
    font=proportional,
)
arp = tk.Checkbutton(
    filter_frame,
    text="ARP",
    variable=arp_checked,
    font=proportional,
)

# ポート番号入力欄を設定
port_frame = tk.Frame(config_frame)
port_label = tk.Label(port_frame, text="ポート番号", font=proportional)
port = tk.Spinbox(
    port_frame,
    from_=0,
    to=65535,
    increment=1,
    font=fixed_width,
)

# IPアドレス入力欄を設定
ipaddress_frame = tk.Frame(config_frame)
ipaddress_label = tk.Label(
    ipaddress_frame,
    text="IPアドレス",
    font=proportional,
)
ipaddress = tk.Entry(ipaddress_frame, font=fixed_width)

# 自動スクロール選択ボタンを設定
autoscroll_checked = tk.BooleanVar()
autoscroll_checked.set(True)

autoscroll = tk.Checkbutton(
    config_frame,
    variable=autoscroll_checked,
    text="自動スクロール",
    font=proportional,
)

# 実行ボタンを設定
buttons_frame = tk.Frame(root)

start_button = tk.Button(buttons_frame, text="開始", font=proportional)
delete_button = tk.Button(buttons_frame, text="消去", font=proportional)

# パケット一覧表示欄を設定
cols = ("時刻", "種別", "送信元IP", "送信元Port", "宛先IP", "宛先Port", "Flags", "Size")

packets_frame = tk.Frame(root)
packets_title = tk.Label(packets_frame, text="パケット一覧", font=proportional)
packets = ttk.Treeview(packets_frame, columns=cols, height=15, show="headings")

for col in cols:
    packets.heading(col, text=col)

yscroll = ttk.Scrollbar(
    packets_frame,
    orient=tk.VERTICAL,
    command=packets.yview,
)
packets.configure(yscroll=yscroll.set)

style = ttk.Style()
style.configure("Treeview", font=fixed_width)
style.configure("Treeview.Heading", font=proportional)

# 16進ダンプ表示欄を設定
hex_dump_frame = tk.Frame(root)
hex_dump_title = tk.Label(
    hex_dump_frame, text="選択パケットの16進ダンプ", font=proportional
)
hex_dump = tk.Text(hex_dump_frame, font=fixed_width)
hex_dump.configure(font=fixed_width)

# root の1列目を伸縮可能に設定
root.grid_columnconfigure(1, weight=1)

# packets_frame 内の列も伸縮可能に
packets_frame.grid_columnconfigure(1, weight=1)
    
# ウィンドウに配置
config_frame.grid(row=1, column=1)
buttons_frame.grid(row=1, column=5, padx=100)
packets_frame.grid(row=5, column=1, sticky="nsew", columnspan=5)
hex_dump_frame.grid(row=9, column=1)

# 設定フレームに配置
combo.grid(row=1, column=1)
filter_frame.grid(row=1, column=5)
port_frame.grid(row=5, column=1)
ipaddress_frame.grid(row=5, column=5)
autoscroll.grid(row=1, column=9)

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
ipaddress.grid(row=5, column=1)

# ボタンフレームに配置
start_button.grid(row=1, column=1)
delete_button.grid(row=5, column=1)

# パケット一覧フレームに配置
packets_title.grid(row=1, column=1)
packets.grid(row=5, column=1, sticky="nsew")
yscroll.grid(row=5, column=5, sticky="ns")

# 16進ダンプフレームに配置
hex_dump_title.grid(row=1, column=1)
hex_dump.grid(row=5, column=1)

root.mainloop()
