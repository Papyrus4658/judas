import tkinter as tk


class Window:
    def __init__(self):
        # メインウィンドウの設定
        self.win = tk.Tk()
        self.max_width = self.win.winfo_screenwidth()
        self.max_height = self.win.winfo_screenheight()
        self.win.geometry(f"{self.max_width}x{self.max_height}")
        self.win.resizable(False, False)
        self.win.title("Judas")

        self.menubar = tk.Menu(self.win)
