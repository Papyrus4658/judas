import tkinter as tk


def create_radio_column(parent, data_list, col_index, shared_var):
    """
    指定されたリストの要素からRadiobuttonを作成し、
    一列（column）に縦に配置する関数
    """
    # enumerateでインデックスと要素を同時に取得
    for row_index, item in enumerate(data_list):
        rb = tk.Radiobutton(
            parent,
            text=item,
            variable=shared_var,  # 3つのリストすべてで共有する変数
            value=f"{col_index}_{item}",  # 選択されたときにどのボタンか特定できる値にする
        )
        #  ここがポイント！ rowをインデックス(row_index)で変化させる！
        # sticky='w' でセル内で左寄せにして見栄えを良く
        rb.grid(row=row_index, column=col_index, sticky="w", padx=10)


# --- 実行コード ---
root = tk.Tk()
root.title("ラジオボタンの展開例")

List1 = [" リンゴ", " みかん", " ぶどう"]
List2 = [" 車", " 飛行機", " 船"]
List3 = [" 犬", " 猫", " うさぎ"]

# 3つのラジオボタングループで共有する変数（一つの選択肢しか選べないように）
selection_var = tk.StringVar(value="None")

# 各リストを隣り合う列に配置 (column=0, 1, 2)
create_radio_column(root, List1, 0, selection_var)
create_radio_column(root, List2, 1, selection_var)
create_radio_column(root, List3, 2, selection_var)

# 列がウィンドウサイズに合わせて拡大するように設定（オプション）
root.columnconfigure((0, 1, 2), weight=1)

root.mainloop()
