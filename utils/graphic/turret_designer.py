import tkinter as tk
from tkinter import messagebox


# 色の設定を簡単に行うための関数
def set_color(r_spinbox, g_spinbox, b_spinbox, r, g, b):
    r_spinbox.delete(0, tk.END)
    r_spinbox.insert(0, r)
    g_spinbox.delete(0, tk.END)
    g_spinbox.insert(0, g)
    b_spinbox.delete(0, tk.END)
    b_spinbox.insert(0, b)

# 円描画関数
def add_circle(canvas, horizontal_radius_spinbox, vertical_radius_spinbox, x_spinbox, y_spinbox, r_spinbox, g_spinbox,
               b_spinbox, border_var):
    try:
        # 各スピンボックスから値を取得
        horizontal_radius = int(horizontal_radius_spinbox.get())
        vertical_radius = int(vertical_radius_spinbox.get())
        x = int(x_spinbox.get())
        y = int(y_spinbox.get())
        r = int(r_spinbox.get())
        g = int(g_spinbox.get())
        b = int(b_spinbox.get())
        border = border_var.get()

        # 描画する円の色と枠線を決定
        fill_color = f'#{r:02x}{g:02x}{b:02x}'
        outline_color = "black" if border else ""

        # 円（楕円）の描画
        canvas.create_oval(
            x - horizontal_radius, y - vertical_radius,  # 左上の座標
            x + horizontal_radius, y + vertical_radius,  # 右下の座標
            fill=fill_color,
            outline=outline_color
        )
    except ValueError:
        messagebox.showerror("Error", "正しい数値を入力してください。")

# 台形の追加アクション
def add_trapezoid(canvas, top_spinbox, bottom_spinbox, height_spinbox, x_spinbox, y_spinbox, r_spinbox, g_spinbox,
                  b_spinbox, border_var):
    # 各スピンボックスから値を取得
    top = int(top_spinbox.get())
    bottom = int(bottom_spinbox.get())
    height = int(height_spinbox.get())
    x = int(x_spinbox.get())
    y = int(y_spinbox.get())
    r = int(r_spinbox.get())
    g = int(g_spinbox.get())
    b = int(b_spinbox.get())
    border = border_var.get()

    # 台形の頂点を計算して描画
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_polygon(
        x + (bottom - top) // 2, y,  # 上辺左
        x + (bottom - top) // 2 + top, y,  # 上辺右
        x + bottom, y + height,  # 下辺右
        x, y + height,  # 下辺左
        fill=color,
        outline="black" if border else ""
    )
    messagebox.showinfo("Action", "台形が追加されました！")

def add_triangle(canvas, base_spinbox, apex_x_spinbox, height_spinbox, x_spinbox, y_spinbox, r_spinbox, g_spinbox,
                 b_spinbox, border_var):
    # 各スピンボックスから値を取得
    base = int(base_spinbox.get())
    apex_x = int(apex_x_spinbox.get())
    height = int(height_spinbox.get())
    x = int(x_spinbox.get())
    y = int(y_spinbox.get())
    r = int(r_spinbox.get())
    g = int(g_spinbox.get())
    b = int(b_spinbox.get())
    border = border_var.get()

    # 三角形の頂点を計算して描画
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_polygon(
        x, y + height,  # 左下
           x + base, y + height,  # 右下
           x + apex_x, y,  # 頂点
        fill=color,
        outline="black" if border else ""
    )
    messagebox.showinfo("Action", "三角形が追加されました！")

# 台形セクションの作成
def create_trapezoid_section(parent_frame, canvas):
    # LabelFrame の作成
    trapezoid_frame = tk.LabelFrame(parent_frame, text="台形操作", padx=10, pady=5)
    trapezoid_frame.grid(row=0, column=0, padx=10, pady=5)

    # 台形のプロパティ：上辺、下辺、高さ
    tk.Label(trapezoid_frame, text="上辺").grid(row=0, column=0, sticky=tk.W)
    top_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
    top_spinbox.grid(row=0, column=1)
    tk.Label(trapezoid_frame, text="下辺").grid(row=0, column=2, sticky=tk.W)
    bottom_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
    bottom_spinbox.grid(row=0, column=3)
    tk.Label(trapezoid_frame, text="高さ").grid(row=0, column=4, sticky=tk.W)
    height_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
    height_spinbox.grid(row=0, column=5)

    # 位置情報：位置 X, 位置 Y
    tk.Label(trapezoid_frame, text="位置 X").grid(row=1, column=0, sticky=tk.W)
    x_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
    x_spinbox.grid(row=1, column=1)
    tk.Label(trapezoid_frame, text="位置 Y").grid(row=1, column=2, sticky=tk.W)
    y_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
    y_spinbox.grid(row=1, column=3)

    # 色選択用：RGB値
    tk.Label(trapezoid_frame, text="RGB").grid(row=2, column=0, sticky=tk.W)
    r_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=255)
    r_spinbox.grid(row=2, column=1)
    g_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=255)
    g_spinbox.grid(row=2, column=2)
    b_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=255)
    b_spinbox.grid(row=2, column=3)

    # 線の有無
    border_var = tk.BooleanVar()
    tk.Checkbutton(trapezoid_frame, text="ふち線あり", variable=border_var).grid(row=3, column=0, columnspan=2,
                                                                                 sticky=tk.W)

    # 台形追加ボタン
    tk.Button(
        trapezoid_frame,
        text="台形追加",
        command=lambda: add_trapezoid(canvas, top_spinbox, bottom_spinbox, height_spinbox, x_spinbox, y_spinbox,
                                      r_spinbox, g_spinbox, b_spinbox, border_var),
        width=20
    ).grid(row=4, column=0, columnspan=6, pady=10)


# 三角形セクションの作成
def create_triangle_section(parent_frame, canvas):
    # LabelFrame の作成
    triangle_frame = tk.LabelFrame(parent_frame, text="三角形操作", padx=10, pady=5)
    triangle_frame.grid(row=1, column=0, padx=10, pady=5)

    # 三角形のプロパティ：底辺、頂点X、高さ
    tk.Label(triangle_frame, text="底辺").grid(row=0, column=0, sticky=tk.W)
    base_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
    base_spinbox.grid(row=0, column=1)
    tk.Label(triangle_frame, text="頂点X").grid(row=0, column=2, sticky=tk.W)
    apex_x_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
    apex_x_spinbox.grid(row=0, column=3)
    tk.Label(triangle_frame, text="高さ").grid(row=0, column=4, sticky=tk.W)
    height_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
    height_spinbox.grid(row=0, column=5)

    # 位置情報：位置 X, 位置 Y
    tk.Label(triangle_frame, text="位置 X").grid(row=1, column=0, sticky=tk.W)
    x_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
    x_spinbox.grid(row=1, column=1)
    tk.Label(triangle_frame, text="位置 Y").grid(row=1, column=2, sticky=tk.W)
    y_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
    y_spinbox.grid(row=1, column=3)

    # 色選択用：RGB値
    tk.Label(triangle_frame, text="RGB").grid(row=2, column=0, sticky=tk.W)
    r_spinbox = tk.Spinbox(triangle_frame, from_=0, to=255)
    r_spinbox.grid(row=2, column=1)
    g_spinbox = tk.Spinbox(triangle_frame, from_=0, to=255)
    g_spinbox.grid(row=2, column=2)
    b_spinbox = tk.Spinbox(triangle_frame, from_=0, to=255)
    b_spinbox.grid(row=2, column=3)

    # 線の有無
    border_var = tk.BooleanVar()
    tk.Checkbutton(triangle_frame, text="ふち線あり", variable=border_var).grid(row=3, column=0, columnspan=2,
                                                                                sticky=tk.W)

    # 三角形追加ボタン
    tk.Button(
        triangle_frame,
        text="三角形追加",
        command=lambda: add_triangle(canvas, base_spinbox, apex_x_spinbox, height_spinbox, x_spinbox, y_spinbox,
                                     r_spinbox, g_spinbox, b_spinbox, border_var),
        width=20
    ).grid(row=4, column=0, columnspan=6, pady=10)

# 円描画セクションの作成
def create_circle_section(parent_frame, canvas):
    # LabelFrame の作成
    circle_frame = tk.LabelFrame(parent_frame, text="円")
    circle_frame.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

    # 横半径、縦半径入力
    tk.Label(circle_frame, text="横半径").grid(row=0, column=0, sticky=tk.W)
    horizontal_radius_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
    horizontal_radius_spinbox.grid(row=0, column=1)
    tk.Label(circle_frame, text="縦半径").grid(row=1, column=0, sticky=tk.W)
    vertical_radius_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
    vertical_radius_spinbox.grid(row=1, column=1)

    # 中心座標の入力
    tk.Label(circle_frame, text="中心 X").grid(row=2, column=0, sticky=tk.W)
    x_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
    x_spinbox.grid(row=2, column=1)
    tk.Label(circle_frame, text="中心 Y").grid(row=3, column=0, sticky=tk.W)
    y_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
    y_spinbox.grid(row=3, column=1)

    # RGB値入力
    tk.Label(circle_frame, text="RGB").grid(row=4, column=0, sticky=tk.W)
    r_spinbox = tk.Spinbox(circle_frame, from_=0, to=255)
    r_spinbox.grid(row=5, column=1)
    tk.Label(circle_frame, text="R").grid(row=5, column=0, sticky=tk.W)
    g_spinbox = tk.Spinbox(circle_frame, from_=0, to=255)
    g_spinbox.grid(row=6, column=1)
    tk.Label(circle_frame, text="G").grid(row=6, column=0, sticky=tk.W)
    b_spinbox = tk.Spinbox(circle_frame, from_=0, to=255)
    b_spinbox.grid(row=7, column=1)
    tk.Label(circle_frame, text="B").grid(row=7, column=0, sticky=tk.W)

    # 枠線の有無
    border_var = tk.BooleanVar()
    tk.Checkbutton(circle_frame, text="ふち線あり", variable=border_var).grid(row=8, column=0, columnspan=2,
                                                                              sticky=tk.W)

    # 追加ボタン
    tk.Button(
        circle_frame,
        text="追加",
        command=lambda: add_circle(canvas, horizontal_radius_spinbox, vertical_radius_spinbox, x_spinbox, y_spinbox,
                                   r_spinbox, g_spinbox, b_spinbox, border_var)
    ).grid(row=9, column=0, columnspan=2, pady=5)


# UIのメイン関数
def create_turret_ui():
    root = tk.Tk()
    root.title("Turret Designer")

    # ウィンドウサイズ設定
    root.geometry("1000x1000")

    # 描画用キャンバス
    canvas = tk.Canvas(root, width=600, height=600, bg="white")
    canvas.pack(pady=10)

    # コントロールパネル (配置用のフレーム)
    control_panel = tk.Frame(root)
    control_panel.pack()

    # 台形セクションを追加
    create_trapezoid_section(control_panel, canvas)

    # 三角形セクションを追加
    create_triangle_section(control_panel, canvas)

    # 円セクションを追加
    create_circle_section(control_panel, canvas)

    root.mainloop()
# 外部から呼び出された際のエントリーポイント
if __name__ == "__main__":
    create_turret_ui()
