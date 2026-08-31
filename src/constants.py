from datetime import datetime

LOCAL_TZ = datetime.now().astimezone().tzinfo
TIME_FORMAT = "%H:%M:%S.%f"

FONT_SIZE = 16
HTTPS_PORT = 443

PROMPT_SELECT_IFACE = "ネットワークインターフェースを選択"
PROMPT_INPUT_PORT = "ポート番号を入力（空欄可）"
PROMPT_INPUT_IP = "IPアドレスを入力（空欄可）"
SWITCH_AUTOSCROLL = "自動スクロール設定"

START = "開始"
STOP = "停止"
DELETE = "消去"
EXIT = "終了"

COLS = ("時刻", "種別", "送信元IP", "送信元Port", "宛先IP", "宛先Port", "Flags", "Size")

CAPTURED_LIST = "パケット一覧"
HEX_DUMP = "選択パケットの詳細"
PACKET_STRUCTURE = "===Packet Structure===\n"
HEX_DUMP_HEAD = "\n===Hex Dump===\n"

UNABLE_START = "キャプチャを開始できません"
IP_NOT_FORMATTED = "IPアドレスの形式に誤りがあります。"
PORT_NOT_INT = "ポート番号は数値を入力してください。"
