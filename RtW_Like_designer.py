import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageDraw, ImageTk
from pdx_tools.pdx_ssw import ship_types, role_types

import utils.graphic.turret

str_c = "コスト"
str_w = "重量"
st_a = "追加"

# メインアプリケーション
class ShipDesignerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.tier_var = None
        self.title("Ship Designer V1.1.5")
        self.geometry("1200x800")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.exit_fullscreen)
        self.iconbitmap("Anc.ico")
        self.displacement_var = tk.StringVar()
        self.asw_value_var = tk.StringVar()
        self.flight_deck_armor_weight_var = tk.StringVar()
        self.hangar_armor_weight_var = tk.StringVar()
        self.total_aircraft_count_var = tk.StringVar()
        self.asw_value_var = tk.StringVar()
        self.cost_var = tk.StringVar()
        self.engine_weight_var = tk.StringVar()
        self.electronics_type_var = tk.StringVar()
        self.electronics_cost_weight_var = tk.StringVar()
        self.engine_weight_var = tk.StringVar()
        self.side_armor_var = tk.StringVar()
        self.side_extension_weight_var = tk.StringVar()
        self.upper_side_weight_var = tk.StringVar()
        self.deck_armor_weight_var = tk.StringVar()
        self.deck_extension_weight_var = tk.StringVar()
        self.conning_tower_weight_var = tk.StringVar()
        self.turret_top_weight_var = tk.StringVar()
        self.turret_weight_var = tk.StringVar()
        self.secondary_gun_weight_var = tk.StringVar()
        self.armor_weight_var = tk.StringVar()
        self.armor_cost_var = tk.StringVar()
        self.armor_type_var = tk.StringVar()
        self.coverage_rate_var = tk.StringVar()
        self.equipment_weight_var = tk.StringVar()
        self.equipment_cost_var = tk.StringVar()
        self.torpedo_defense_weight_var = tk.StringVar()
        self.torpedo_defense_cost_var = tk.StringVar()
        self.habitation_weight_var = tk.StringVar()
        self.habitation_cost_var = tk.StringVar()
        self.crew_count_var = tk.StringVar()
        self.total_weight_var = tk.StringVar()
        self.total_cost_var = tk.StringVar()
        self.main_gun_weight_var = tk.StringVar()
        self.main_gun_cost_var = tk.StringVar()
        self.aa_guns_weight_var = tk.StringVar()
        self.aa_guns_crew_var = tk.StringVar()
        self.aa_guns_cost_var = tk.StringVar()
        self.secondary_gun_weight_var = tk.StringVar()
        self.secondary_gun_cost_var = tk.StringVar()
        self.tertiary_gun_weight_var = tk.StringVar()
        self.tertiary_gun_cost_var = tk.StringVar()
        self.horsepower_var = tk.StringVar()
        self.trapezoids = []
        self.triangles = []
        self.circles = []
        self.armo_images = []
        self.tier_var = tk.StringVar()

        # メインフレーム
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # スクロールバーを追加
        self.main_canvas = tk.Canvas(self.main_frame)
        self.main_hscrollbar = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.main_canvas.xview)
        self.main_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas)


        self.scrollable_frame.bind("<Configure>",
            lambda e: self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )
        )
        self.main_frame.bind_all("<MouseWheel>", self._on_mousewheel)
        self.main_frame.bind_all("<Button-4>", self._on_mousewheel)
        self.main_frame.bind_all("<Button-5>", self._on_mousewheel)
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set, xscrollcommand=self.main_hscrollbar.set)

        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set, xscrollcommand=self.main_hscrollbar.set)

        self.main_hscrollbar.pack(side="bottom", fill="x")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")

        # 左側パネル
        self.left_panel_container = tk.Frame(self.scrollable_frame)
        self.left_panel_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 上部パネル
        self.upper_panel = tk.Frame(self.left_panel_container)
        self.upper_panel.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=True)

        # 下部パネル
        self.lower_panel = tk.Frame(self.left_panel_container)
        self.lower_panel.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=True)

        # Create a frame to hold the button and the canvas
        self.graphics_frame = tk.Frame(self.scrollable_frame)
        self.graphics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # 初期のキャンバス倍率（ズームスケール）
        self.zoom_scale = 5.0

        self.side_view_button = tk.Button(self.graphics_frame, text="横面")

        # 「+」「-」ボタンを作成
        self.plus_button = tk.Button(self.graphics_frame, text="+", command=self.zoom_in)
        self.plus_button.pack(side=tk.TOP, fill=tk.X)
        self.minus_button = tk.Button(self.graphics_frame, text="-", command=self.zoom_out)
        self.minus_button.pack(side=tk.TOP, fill=tk.X)

        # Graphics area
        self.graphics_canvas = tk.Canvas(self.graphics_frame, bg="#bce2e8")
        self.graphics_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Upper panel
        self.upper_panel = tk.Frame(self.left_panel_container)
        self.upper_panel.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=True)

        # Lower panel
        self.lower_panel = tk.Frame(self.left_panel_container)
        self.lower_panel.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=True)

        # 左側：全般設定
        self.create_general_settings(self.upper_panel)

        # 右側：タブで切り替えられる詳細設定
        self.create_tabbed_interface(self.lower_panel)



    def zoom_in(self):
        """Increase the zoom scale and update the canvas."""
        self.zoom_scale += 0.2  # Increase zoom scale
        self.update_lines()  # Redraw the canvas

    def zoom_out(self):
        """Decrease the zoom scale (without going below a limit) and update the canvas."""
        if self.zoom_scale > 2.5:  # Ensure zoom level stays above 2.5
            self.zoom_scale -= 0.2  # Decrease zoom scale
        self.update_lines()  # Redraw the canvas
    #中央の♦️を描画
    def draw_diamond(self):
        canvas_width = self.graphics_canvas.winfo_width()
        canvas_height = self.graphics_canvas.winfo_height()
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        size = 2*self.zoom_scale  # Size of the diamond

        points = [
            center_x, center_y - size,  # Top
                      center_x + size, center_y,  # Right
            center_x, center_y + size,  # Bottom
                      center_x - size, center_y   # Left
        ]

        self.graphics_canvas.create_polygon(points, fill="red", outline="black")
    #フルスクリーン解除
    def exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)
    #画像保存
    def save_canvas_as_png(self):
        # Get the canvas dimensions
        canvas_width = self.graphics_canvas.winfo_width()
        canvas_height = self.graphics_canvas.winfo_height()

        # Create a new image with a transparent background
        image = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw the canvas content onto the image
        for item in self.graphics_canvas.find_all():
            coords = self.graphics_canvas.coords(item)
            item_type = self.graphics_canvas.type(item)
            # if item_type == "polygon":
            #     fill = self.graphics_canvas.itemcget(item, "fill")
            #     outline = self.graphics_canvas.itemcget(item, "outline")
            #     draw.polygon(coords, fill=fill, outline=outline)
            if item_type == "line":
                fill = self.graphics_canvas.itemcget(item, "fill")
                width = int(float(self.graphics_canvas.itemcget(item, "width")))
                draw.line(coords, fill=fill, width=width)

        # Ask the user to select a directory to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            image.save(file_path, "PNG")
            messagebox.showinfo("Success", "Image saved successfully.")
    #ズームイン/アウトの実質的処理
    def update_canvas_size(self, event=None):
        # ウィンドウ幅と高さを取得
        window_width = self.graphics_frame.winfo_width()  # グラフィックエリアの幅
        window_height = self.graphics_frame.winfo_height()  # グラフィックエリアの高さ

        # スクロールバーの幅を取得 (ほとんどの場合 17px を想定)
        scrollbar_width = self.main_scrollbar.winfo_width()

        # キャンバスサイズを計算して反映
        self.graphics_canvas.config(
            width=window_width - scrollbar_width,  # スクロールバー分を差し引く
            height=window_height
        )

        # キャンバスの再描画 (update_lines をリサイズ時にも呼び出し)
        self.update_lines()
    #描画処理
    def update_lines(self, event=None):
        canvas_width = self.graphics_canvas.winfo_width()
        canvas_height = self.graphics_canvas.winfo_height()

        canvas_center_x = canvas_width // 2
        canvas_center_y = canvas_height // 2
        scale = 10

        try:
            length_value = float(self.length_spinbox.get())
            width_value = float(self.width_spinbox.get())
        except ValueError:
            length_value = 100.0
            width_value = 50.0

        scaled_length = int(length_value * self.zoom_scale)
        scaled_width = int(width_value * self.zoom_scale)
        scaled_scale = int(scale * self.zoom_scale)

        self.graphics_canvas.delete("all")

        self.graphics_canvas.create_line(
            canvas_center_x, canvas_center_y - scaled_length // 2,
            canvas_center_x, canvas_center_y + scaled_length // 2,
            fill="black", width=2
        )

        self.graphics_canvas.create_line(
            canvas_center_x - scaled_width // 2, canvas_center_y,
            canvas_center_x + scaled_width // 2, canvas_center_y,
            fill="black", width=2
        )



        hull_top = canvas_center_y - scaled_length // 2
        hull_bottom = canvas_center_y + scaled_length // 2

        section_ratios = [2,1,2,3,2,3,3,2,2]
        section_heights = [scaled_length * ratio / sum(section_ratios) for ratio in section_ratios]

        positions = [hull_bottom]
        for height in section_heights:
            positions.append(positions[-1] - height)

        widths = [0, scaled_width*3/5, scaled_width*4/5, scaled_width, scaled_width,
                  scaled_width, scaled_width*6/7, scaled_width*5/7, scaled_width*3/7, 0]

        colors = ["#cccccc","#cccccc","#deb887","#deb887","#deb887","#deb887","#deb887","#deb887","#cccccc","#cccccc"]
        def draw_section_lines(start_y, end_y, start_width, end_width, color):
            y_positions = list(range(int(start_y), int(end_y) - 1, -1)) if start_y >= end_y else list(
                range(int(start_y), int(end_y) + 1))

            for i, y in enumerate(y_positions):
                current_width = start_width - (start_width - end_width) * (i / max(len(y_positions) - 1, 1))
                start_x = canvas_center_x - int(current_width / 2)
                end_x = canvas_center_x + int(current_width / 2)

                self.graphics_canvas.create_line(
                    start_x, y, end_x, y, fill=color, width=2, capstyle="round"
                )

                if current_width > 0:
                    self.graphics_canvas.create_line(start_x, y, start_x +4, y, fill="#cccccc", width=2, capstyle="round")
                    self.graphics_canvas.create_line(end_x - 4, y, end_x, y, fill="#cccccc", width=2, capstyle="round")
                    self.graphics_canvas.create_line(end_x - 1, y, end_x, y, fill="#000000", width=2, capstyle="round")
                    self.graphics_canvas.create_line(start_x, y, start_x + 1, y, fill="#000000", width=2, capstyle="round")

        # def draw_alternate_vertical_lines(start_y, end_y, start_width, end_width):
        #     y_positions = list(range(int(start_y), int(end_y) - 1, -1)) if start_y >= end_y else list(
        #         range(int(start_y), int(end_y) + 1))
        #     #c2955c
        #     colors = ["#deb887", "#deb887"]
        #
        #     for i, y in enumerate(y_positions):
        #         current_width = start_width - (start_width - end_width) * (i / max(len(y_positions) - 1, 1))
        #         start_x = canvas_center_x - int(current_width / 2)
        #         end_x = canvas_center_x + int(current_width / 2)
        #
        #         for x in range(start_x, end_x, 2):
        #             color = colors[(x - start_x) % 4 // 2]
        #             self.graphics_canvas.create_line(x, y, x + 1, y, fill=color, width=2)

        for i in range(len(positions) - 1):
            draw_section_lines(positions[i], positions[i + 1], widths[i], widths[i + 1], colors[i])
            # draw_alternate_vertical_lines(positions[i], positions[i + 1], widths[i], widths[i + 1])
        for trapezoid in self.trapezoids:
            self.draw_trapezoid(trapezoid)
        for triangle in self.triangles:
            self.draw_triangle(triangle)
        for circle in self.circles:
            self.draw_circle(circle)
        for image in self.armo_images:
            self.draw_images()
        # self.draw_diamond()

    def draw_images(self):
        modules_dir = "utils/database/modules"
        canvas_center_x = self.graphics_canvas.winfo_width() // 2
        canvas_center_y = self.graphics_canvas.winfo_height() // 2
        for image in self.armo_images:
            image_path = os.path.join(modules_dir, image["image_name"])
            scaled_width = int(image["scaled_width"] * self.zoom_scale)
            scaled_height = int(image["scaled_height"] * self.zoom_scale)
            x = int(image["position"]["x"] * self.zoom_scale) + canvas_center_x
            y = int(image["position"]["y"] * self.zoom_scale) + canvas_center_y
            ang = image["angle"]
            try:
                img = Image.open(image_path)
                img = img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
                img = img.rotate(ang, expand=True)  # 画像を指定された角度で回転
                tk_img = ImageTk.PhotoImage(img)
                self.graphics_canvas.create_image(x, y, image=tk_img, anchor=tk.NW)
                if not hasattr(self.graphics_canvas, 'images'):
                    self.graphics_canvas.images = []
                self.graphics_canvas.images.append(tk_img)  # 参照を保持してガベージコレクションを防ぐ
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
    #マウスホイールの対応
    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.main_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.main_canvas.yview_scroll(1, "units")
    #ステータス編集画面
    def create_general_settings(self, parent):
        # 艦種

        defo_l = 215.8
        defo_w = 28.96
        intVar = tk.IntVar(value = defo_l)
        intVar2 = tk.IntVar(value = defo_w)
        tk.Label(parent, text="大艦種").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(parent,state='readonly', values=ship_types).grid(row=0, column=1)
        tk.Label(parent, text="詳細艦種").grid(row=0, column=2, sticky=tk.W)
        ttk.Combobox(parent,state='readonly',values = role_types ).grid(row=0, column=3)
        tk.Label(parent, text="国家選択").grid(row=0, column=4, sticky=tk.W)
        ttk.Combobox(parent,state='readonly', values=["USA", "UK", "Japan"]).grid(row=0, column=5)
        tk.Button(parent, text="画像書き出し",command=self.save_canvas_as_png).grid(row=0, column=6)

        # 艦級
        tk.Label(parent, text="艦級").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(parent).grid(row=1, column=1)
        tk.Button(parent, text="艦級名提案").grid(row=1, column=2)
        tk.Button(parent, text="リセット").grid(row=1, column=3)

        # 排水量
        tk.Label(parent, text="排水量").grid(row=2, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100000).grid(row=2, column=1)

        # Create Spinboxes for 全長 and 全幅
        tk.Label(parent, text="全長").grid(row=2, column=2, sticky=tk.W)
        self.length_spinbox = tk.Spinbox(parent, from_=0, to=1000,textvariable = intVar)
        self.length_spinbox.grid(row=2, column=3)

        tk.Label(parent, text="全幅").grid(row=2, column=4, sticky=tk.W)
        self.width_spinbox = tk.Spinbox(parent, from_=0, to=100, textvariable = intVar2)
        self.width_spinbox.grid(row=2, column=5)
        tk.Button(parent, text="描画更新", command=self.update_lines).grid(row=2, column=6)

        # アルミニウム製上部構造
        tk.Checkbutton(parent, text="アルミニウム製上部構造").grid(row=3, column=0, columnspan=2, sticky=tk.W)

        # 船体
        tk.Label(parent, text="船体").grid(row=4, column=0, sticky=tk.W)
        ttk.Combobox(parent,state='readonly', values=["Type A", "Type B"]).grid(row=4, column=1)
        tk.Label(parent, text="常備排水量").grid(row=4, column=2, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100000).grid(row=4, column=3)
        tk.Label(parent, text="排水量").grid(row=4, column=4, sticky=tk.W)
        tk.Label(parent, textvariable=self.displacement_var).grid(row=4, column=5)
        tk.Label(parent, text=str_c).grid(row=4, column=6, sticky=tk.W)
        tk.Label(parent, textvariable=self.cost_var).grid(row=4, column=7)

        # 速力
        tk.Label(parent, text="速力").grid(row=5, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=5, column=1)
        tk.Label(parent, text="航続距離").grid(row=5, column=3, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=10000).grid(row=5, column=4)

        # 馬力
        tk.Label(parent, text="馬力").grid(row=6, column=0, sticky=tk.W)
        tk.Label(parent, textvariable=self.horsepower_var).grid(row=6, column=1)
        tk.Label(parent, text="機関重量").grid(row=6, column=2, sticky=tk.W)
        tk.Label(parent, textvariable=self.engine_weight_var).grid(row=6, column=3)

        # エンジンの優先順位
        tk.Label(parent, text="エンジンの優先順位").grid(row=7, column=0, sticky=tk.W)
        ttk.Combobox(parent,state='readonly', values=["Priority A", "Priority B"]).grid(row=7, column=1)
        tk.Label(parent, text="燃料").grid(row=7, column=2, sticky=tk.W)
        ttk.Combobox(parent,state='readonly', values=["Oil", "Coal"]).grid(row=7, column=3)
        tk.Checkbutton(parent, text="シフト配置").grid(row=7, column=4, columnspan=2, sticky=tk.W)

        # 舷側装甲
        tk.Label(parent, text="舷側装甲").grid(row=8, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=8, column=1)
        tk.Checkbutton(parent, text="弾薬庫装甲").grid(row=8, column=3, columnspan=2, sticky=tk.W)
        tk.Label(parent, textvariable=self.side_armor_var).grid(row=8, column=5)

        # 舷側延長
        tk.Label(parent, text="舷側延長").grid(row=9, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=9, column=1)
        tk.Label(parent, text=str_w).grid(row=9, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.side_extension_weight_var).grid(row=9, column=4)

        # 舷側上部
        tk.Label(parent, text="舷側上部").grid(row=10, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=10, column=1)
        tk.Label(parent, text=str_w).grid(row=10, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.upper_side_weight_var).grid(row=10, column=4)

        # 甲板装甲
        tk.Label(parent, text="甲板装甲").grid(row=11, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=11, column=1)
        tk.Label(parent, text=str_w).grid(row=11, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.deck_armor_weight_var).grid(row=11, column=4)

        # 甲板延長
        tk.Label(parent, text="甲板延長").grid(row=12, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=12, column=1)
        tk.Label(parent, text=str_w).grid(row=12, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.deck_extension_weight_var).grid(row=12, column=4)

        # 司令塔
        tk.Label(parent, text="司令塔").grid(row=13, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=13, column=1)
        tk.Label(parent, text=str_w).grid(row=13, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.conning_tower_weight_var).grid(row=13, column=4)

        # 砲塔上部
        tk.Label(parent, text="砲塔上部").grid(row=14, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=14, column=1)
        tk.Label(parent, text=str_w).grid(row=14, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.turret_top_weight_var).grid(row=14, column=4)

        # 砲塔
        tk.Label(parent, text="砲塔").grid(row=15, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=15, column=1)
        tk.Label(parent, text=str_w).grid(row=15, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.turret_weight_var).grid(row=15, column=4)

        # 副砲
        tk.Label(parent, text="副砲").grid(row=16, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=16, column=1)
        tk.Label(parent, text=str_w).grid(row=16, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.secondary_gun_weight_var).grid(row=16, column=4)

        # 装甲重量
        tk.Label(parent, text="装甲重量").grid(row=17, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.armor_weight_var).grid(row=17, column=4)
        tk.Label(parent, text=str_c).grid(row=17, column=5, sticky=tk.W)
        tk.Label(parent, textvariable=self.armor_cost_var).grid(row=17, column=6)

        # 装甲種別
        tk.Label(parent, text="装甲種別").grid(row=18, column=0, sticky=tk.W)
        tk.Label(parent, textvariable=self.armor_type_var).grid(row=18, column=1)
        tk.Label(parent, text="カバー率").grid(row=18, column=2, sticky=tk.W)
        tk.Label(parent, textvariable=self.coverage_rate_var).grid(row=18, column=3)

        # 装備重量
        tk.Label(parent, text="装備重量").grid(row=19, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.equipment_weight_var).grid(row=19, column=4)
        tk.Label(parent, text=str_c).grid(row=19, column=5, sticky=tk.W)
        tk.Label(parent, textvariable=self.equipment_cost_var).grid(row=19, column=6)

        # 水雷防御レベル
        tk.Label(parent, text="水雷防御レベル").grid(row=20, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=20, column=1)
        tk.Label(parent, text=str_w).grid(row=20, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.torpedo_defense_weight_var).grid(row=20, column=4)
        tk.Label(parent, text=str_c).grid(row=20, column=5, sticky=tk.W)
        tk.Label(parent, textvariable=self.torpedo_defense_cost_var).grid(row=20, column=6)

        # 居住区レベル
        tk.Label(parent, text="居住区レベル").grid(row=21, column=0, sticky=tk.W)
        tk.Spinbox(parent, from_=0, to=100).grid(row=21, column=1)
        tk.Label(parent, text=str_w).grid(row=21, column=3, sticky=tk.W)
        tk.Label(parent, textvariable=self.habitation_weight_var).grid(row=21, column=4)
        tk.Label(parent, text=str_c).grid(row=21, column=5, sticky=tk.W)
        tk.Label(parent, textvariable=self.habitation_cost_var).grid(row=21, column=6)

        # 乗員数
        tk.Label(parent, text="乗員数").grid(row=22, column=0, sticky=tk.W)
        tk.Label(parent, textvariable=self.crew_count_var).grid(row=22, column=1)
        tk.Label(parent, text="総重量").grid(row=22, column=2, sticky=tk.W)
        tk.Label(parent, textvariable=self.total_weight_var).grid(row=22, column=3)
        tk.Label(parent, text="総コスト").grid(row=22, column=4, sticky=tk.W)
        tk.Label(parent, textvariable=self.total_cost_var).grid(row=22, column=5)

        # 植民地用
        tk.Checkbutton(parent, text="植民地用").grid(row=23, column=0, columnspan=2, sticky=tk.W)
    #タブ作成
    def create_tabbed_interface(self, parent):
        # タブを作成
        tab_control = ttk.Notebook(parent)

        # 各タブ
        self.guns_tab = ttk.Frame(tab_control)
        self.additional_armament_tab = ttk.Frame(tab_control)
        self.graphics_tab = ttk.Frame(tab_control)

        tab_control.add(self.guns_tab, text="備砲")
        tab_control.add(self.additional_armament_tab, text="その他の装備")
        tab_control.add(self.graphics_tab, text="グラフィック")

        tab_control.pack(expand=True, fill=tk.BOTH)

        # Gunsタブ
        self.create_guns_tab(self.guns_tab)
        self.create_additional_armament_tab(self.additional_armament_tab)
        self.create_graphics_tab(self.graphics_tab)
    #備砲タブ
    def create_guns_tab(self, parent):
        self.create_main_guns_section(parent)
        self.create_aa_guns_section(parent)
        self.create_secondary_guns_section(parent)
        self.create_tertiary_guns_section(parent)
    def show_turret(self):
        utils.show_turret_data(self)
    #主砲セクション
    def create_main_guns_section(self, parent):
        # 主武装セクション (左上)
        main_guns_frame = tk.LabelFrame(parent, text="主武装")
        main_guns_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)

        # 口径
        tk.Label(main_guns_frame, text="口径").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Spinbox(main_guns_frame, from_=0, to=100).grid(row=0, column=1)
        tk.Button(main_guns_frame, text="砲塔データ", command=self.show_turret).grid(row=0, column=2)

        # 主砲詳細
        tree_frame = tk.Frame(main_guns_frame)
        tree_frame.grid(row=2, column=0, columnspan=4, pady=5, sticky=tk.NSEW)
        self.details_list = ttk.Treeview(tree_frame, columns=("位置", "門数", "重量", "人員"), show="headings", height=10)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.details_list.xview)
        self.details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.details_list.heading("位置", text="位置")
        self.details_list.heading("門数", text="門数")
        self.details_list.heading("重量", text="重量")
        self.details_list.heading("人員", text="人員")
        self.details_list.column("位置", width=100)
        self.details_list.column("門数", width=100)
        self.details_list.column("重量", width=100)
        self.details_list.column("人員", width=100)

        # 追加、削除、全削除ボタン
        tk.Button(main_guns_frame, text="追加").grid(row=3, column=0, pady=5)
        tk.Button(main_guns_frame, text="削除").grid(row=3, column=1, pady=5)
        tk.Button(main_guns_frame, text="全削除").grid(row=3, column=2, pady=5)

        # FCS
        tk.Label(main_guns_frame, text="FCS:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(main_guns_frame, values=["FCS Type 1", "FCS Type 2"]).grid(row=4, column=1)
        tk.Label(main_guns_frame, text="基数").grid(row=4, column=2, sticky=tk.W, pady=5)
        tk.Spinbox(main_guns_frame, from_=0, to=100).grid(row=4, column=3)

        # 重量とコスト
        tk.Label(main_guns_frame, text="重量").grid(row=5, column=0, sticky=tk.W, pady=5)
        tk.Label(main_guns_frame, textvariable=self.main_gun_weight_var).grid(row=5, column=1)
        tk.Label(main_guns_frame, text="コスト").grid(row=5, column=2, sticky=tk.W, pady=5)
        tk.Label(main_guns_frame, textvariable=self.main_gun_cost_var).grid(row=5, column=3)

        # ティア
        tk.Label(main_guns_frame, text="ティア:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(main_guns_frame, textvariable=self.tier_var, values=["1", "2"]).grid(row=6, column=1)

        # 左右非対称砲塔チェックボックス
        tk.Checkbutton(main_guns_frame, text="左右非対称砲塔").grid(row=7, column=0, columnspan=3, sticky=tk.W)
    #対空火器セクション
    def create_aa_guns_section(self, parent):
        # 対空火器セクション (左下)
        aa_guns_frame = tk.LabelFrame(parent, text="対空火器")
        aa_guns_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.SW)

        # 種類、基数、追加ボタン
        tk.Label(aa_guns_frame, text="種類").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(aa_guns_frame, values=["Type 1", "Type 2"]).grid(row=0, column=1)
        tk.Label(aa_guns_frame, text="基数").grid(row=0, column=2, sticky=tk.W, pady=5)
        tk.Spinbox(aa_guns_frame, from_=0, to=100).grid(row=0, column=3)
        tk.Button(aa_guns_frame, text=st_a).grid(row=0, column=4)

        # リスト

        tree_frame = tk.Frame(aa_guns_frame)
        tree_frame.grid(row=2, column=0, columnspan=4, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("種類", "基数", str_w, "人員"), show="headings", height=10)
        details_list.column("種類", width=50)
        details_list.column("基数", width=50)
        details_list.column(str_w, width=50)
        details_list.column("人員", width=50)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_list.heading("種類", text="種類")
        details_list.heading("基数", text="基数")
        details_list.heading(str_w, text=str_w)
        details_list.heading("人員", text="人員")

        # 合計
        tk.Label(aa_guns_frame, text="合計").grid(row=3, column=0, sticky=tk.W, pady=5)
        tk.Label(aa_guns_frame, text=str_w).grid(row=3, column=1, sticky=tk.W, pady=5)
        tk.Label(aa_guns_frame, textvariable=self.aa_guns_weight_var).grid(row=3, column=2)
        tk.Label(aa_guns_frame, text="人員").grid(row=3, column=3, sticky=tk.W, pady=5)
        tk.Label(aa_guns_frame, textvariable=self.aa_guns_crew_var).grid(row=3, column=4)
        tk.Label(aa_guns_frame, text=str_c).grid(row=3, column=5, sticky=tk.W, pady=5)
        tk.Label(aa_guns_frame, textvariable=self.aa_guns_cost_var).grid(row=3, column=6)
    #副砲セクション
    def create_secondary_guns_section(self, parent):
        # 副砲セクション (右上)
        secondary_guns_frame = tk.LabelFrame(parent, text="副砲")
        secondary_guns_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NE)

        # 既存要素
        tk.Label(secondary_guns_frame, text="口径").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Spinbox(secondary_guns_frame, from_=0, to=100).grid(row=0, column=1)
        tk.Label(secondary_guns_frame, text="門数").grid(row=0, column=2, sticky=tk.W, pady=5)
        tk.Spinbox(secondary_guns_frame, from_=0, to=100).grid(row=0, column=3)
        tk.Button(secondary_guns_frame, text="砲塔データ").grid(row=0, column=4)

        # 砲身数、ティア、追加ボタン
        tk.Label(secondary_guns_frame, text="砲身数").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Spinbox(secondary_guns_frame, from_=0, to=100).grid(row=1, column=1)
        tk.Label(secondary_guns_frame, text="ティア").grid(row=1, column=2, sticky=tk.W, pady=5)
        ttk.Combobox(secondary_guns_frame, values=["Tier 1", "Tier 2"]).grid(row=1, column=3)
        tk.Button(secondary_guns_frame, text=st_a).grid(row=1, column=4)

        # 副砲リスト
        tree_frame = tk.Frame(secondary_guns_frame)
        tree_frame.grid(row=2, column=0, columnspan=5, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("種類", "門数", str_w, "人員"), show="headings", height=10)
        details_list.column("種類", width=50)
        details_list.column("門数", width=50)
        details_list.column(str_w, width=50)
        details_list.column("人員", width=50)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_list.heading("種類", text="種類")
        details_list.heading("門数", text="門数")
        details_list.heading(str_w, text=str_w)
        details_list.heading("人員", text="人員")

        # 非対称配置チェックボックス、自動配置ボタン
        tk.Checkbutton(secondary_guns_frame, text="非対称配置").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        tk.Button(secondary_guns_frame, text="自動配置").grid(row=3, column=2, columnspan=3, sticky=tk.W, pady=5)

        #重量・コスト
        tk.Label(secondary_guns_frame, text=str_w).grid(row=4, column=0, sticky=tk.W, pady=5)
        tk.Label(secondary_guns_frame, textvariable=self.secondary_gun_weight_var).grid(row=4, column=1)
        tk.Label(secondary_guns_frame, text=str_c).grid(row=4, column=2, sticky=tk.W, pady=5)
        tk.Label(secondary_guns_frame, textvariable=self.secondary_gun_cost_var).grid(row=4, column=1)
    #三次砲セクション
    def create_tertiary_guns_section(self, parent):
        # 三次砲セクション (右下)
        tertiary_guns_frame = tk.LabelFrame(parent, text="三次砲")
        tertiary_guns_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.SE)

        # 既存要素
        tk.Label(tertiary_guns_frame, text="口径").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Spinbox(tertiary_guns_frame, from_=0, to=100).grid(row=0, column=1)
        tk.Label(tertiary_guns_frame, text="門数").grid(row=0, column=2, sticky=tk.W, pady=5)
        tk.Spinbox(tertiary_guns_frame, from_=0, to=100).grid(row=0, column=3)
        tk.Button(tertiary_guns_frame, text="砲塔データ").grid(row=0, column=4)

        # 砲身数、ティア、追加ボタン
        tk.Label(tertiary_guns_frame, text="砲身数").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Spinbox(tertiary_guns_frame, from_=0, to=100).grid(row=1, column=1)
        tk.Label(tertiary_guns_frame, text="ティア").grid(row=1, column=2, sticky=tk.W, pady=5)
        ttk.Combobox(tertiary_guns_frame, values=["Tier 1", "Tier 2"]).grid(row=1, column=3)
        tk.Button(tertiary_guns_frame, text=st_a).grid(row=1, column=4)
        # 三次砲リスト
        tree_frame = tk.Frame(tertiary_guns_frame)
        tree_frame.grid(row=2, column=0, columnspan=5, pady=5)
        tree_frame.grid_propagate(False)  # フレームのサイズを固定
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        details_list = ttk.Treeview(
            tree_frame, columns=("種類", "門数", str_w, "人員"), show="headings", height=10
        )
        details_list.column("種類", width=100)
        details_list.column("門数", width=50)
        details_list.column(str_w, width=50)
        details_list.column("人員", width=50)
        details_list.pack(fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)

        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # スクロールバーを配置
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    #その他装備タブ
    def create_additional_armament_tab(self,parent):
        # 2列のグリッドフレーム
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 1列目 (Left) と 2列目 (Right)

        # 1行目: Torpedo と Aircraft
        self.create_torpedo_section(frame).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.create_aircraft_section(frame).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # 2行目: Mine と Catapult
        self.create_mine_section(frame).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.create_catapult_section(frame).grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # 3行目: ASW と Missile
        self.create_asw_section(frame).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.create_missile_section(frame).grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # 最終行: Electronics (中央配置)
        self.create_electronics_section(frame).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # グリッドの拡張設定
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
    #魚雷セクション
    def create_torpedo_section(self, parent):
        torpedo_frame = tk.LabelFrame(parent, text="魚雷")
        tk.Label(torpedo_frame, text="種類").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(torpedo_frame, values=["Type 1", "Type 2", "Type 3"]).grid(row=0, column=1)
        tk.Label(torpedo_frame, text="基数").grid(row=0, column=2, sticky=tk.W)
        tk.Spinbox(torpedo_frame, from_=0, to=100).grid(row=0, column=3)
        tree_frame = tk.Frame(torpedo_frame)
        tree_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("位置", "種類", str_w, "人員"), show="headings", height=10)
        details_list.heading("位置", text="位置")
        details_list.heading("種類", text="種類")
        details_list.heading(str_w, text=str_w)
        details_list.heading("人員", text="人員")
        details_list.column("位置", width=100)
        details_list.column("種類", width=100)
        details_list.column(str_w, width=100)
        details_list.column("人員", width=100)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Button(torpedo_frame, text=st_a).grid(row=2, column=0, pady=5)
        tk.Button(torpedo_frame, text="削除").grid(row=2, column=1, pady=5)
        tk.Button(torpedo_frame, text="全削除").grid(row=2, column=2, pady=5)
        tk.Checkbutton(torpedo_frame, text="自動装填装置").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

        return torpedo_frame
    #機雷
    def create_mine_section(self, parent):
        mine_frame = tk.LabelFrame(parent, text="機雷")
        tk.Label(mine_frame, text="種類").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(mine_frame, values=["Moored Mine", "Drifting Mine"]).grid(row=0, column=1)
        tk.Label(mine_frame, text="機雷数").grid(row=1, column=0, sticky=tk.W)
        tk.Spinbox(mine_frame, from_=0, to=100).grid(row=1, column=1)
        tk.Label(mine_frame, text="掃海装置").grid(row=2, column=0, sticky=tk.W)
        ttk.Combobox(mine_frame, values=["Sweep Gear A", "Sweep Gear B", "Sweep Gear C"]).grid(row=2, column=1)

        return mine_frame
    #対潜装備
    def create_asw_section(self, parent):
        asw_frame = tk.LabelFrame(parent, text="対潜")
        ttk.Combobox(asw_frame, values=["DC", "Torpedo Depth Charge", "Sonar Buoy"]).grid(row=0, column=1)
        tk.Label(asw_frame, text="基数").grid(row=0, column=2, sticky=tk.W)
        tk.Spinbox(asw_frame, from_=0, to=100).grid(row=0, column=3)
        tree_frame = tk.Frame(asw_frame)
        tree_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("位置", "種類", str_w, "人員"), show="headings", height=10)
        details_list.heading("位置", text="位置")
        details_list.heading("種類", text="種類")
        details_list.heading(str_w, text=str_w)
        details_list.heading("人員", text="人員")
        details_list.column("位置", width=100)
        details_list.column("種類", width=100)
        details_list.column(str_w, width=100)
        details_list.column("人員", width=100)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Button(asw_frame, text=st_a).grid(row=2, column=0, pady=5)
        tk.Button(asw_frame, text="削除").grid(row=2, column=1, pady=5)
        tk.Button(asw_frame, text="全削除").grid(row=2, column=2, pady=5)
        tk.Label(asw_frame, text="対潜値").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.asw_value_var = tk.StringVar()
        tk.Label(asw_frame, textvariable=self.asw_value_var).grid(row=3, column=1, sticky=tk.W)

        return asw_frame
    #電装
    def create_electronics_section(self, parent):
        electronics_frame = tk.LabelFrame(parent, text="電装")
        tk.Label(electronics_frame, text="装置").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(electronics_frame, values=["Radar", "Sonar", "Electronic Systems"]).grid(row=0, column=1)
        tk.Label(electronics_frame, text="種類を選択").grid(row=1, column=0, sticky=tk.W)
        self.electronics_type_var = tk.StringVar()
        ttk.Combobox(electronics_frame, textvariable=self.electronics_type_var, values=["Type A", "Type B", "Type C"]).grid(row=1, column=1)
        tk.Label(electronics_frame, text="コスト/重量").grid(row=2, column=0, sticky=tk.W)
        self.electronics_cost_weight_var = tk.StringVar()
        tk.Label(electronics_frame, textvariable=self.electronics_cost_weight_var).grid(row=2, column=1)

        return electronics_frame
    #航空機
    def create_aircraft_section(self, parent):
        aircraft_frame = tk.LabelFrame(parent, text="航空")
        tk.Label(aircraft_frame, text="種類選択").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(aircraft_frame, values=["Recon Plane", "Fighter", "Torpedo Bomber"]).grid(row=0, column=1)
        tk.Label(aircraft_frame, text="基数").grid(row=0, column=2, sticky=tk.W)
        tk.Spinbox(aircraft_frame, from_=0, to=100).grid(row=0, column=3)
        tree_frame = tk.Frame(aircraft_frame)
        tree_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("種類", str_w, "人員"), show="headings", height=10)
        details_list.heading("種類", text="種類")
        details_list.heading(str_w, text=str_w)
        details_list.heading("人員", text="人員")
        details_list.column("種類", width=100)
        details_list.column(str_w, width=100)
        details_list.column("人員", width=100)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Button(aircraft_frame, text="追加ボタン").grid(row=2, column=0, pady=5)
        tk.Button(aircraft_frame, text="削除ボタン").grid(row=2, column=1, pady=5)
        tk.Button(aircraft_frame, text="全削除ボタン").grid(row=2, column=2, pady=5)
        tk.Label(aircraft_frame, text="飛行甲板装甲").grid(row=3, column=0, sticky=tk.W)
        tk.Spinbox(aircraft_frame, from_=0, to=100).grid(row=3, column=1)
        tk.Label(aircraft_frame, text=str_w).grid(row=3, column=2, sticky=tk.W)
        tk.Label(aircraft_frame, textvariable=self.flight_deck_armor_weight_var).grid(row=3, column=3)
        tk.Label(aircraft_frame, text="格納庫装甲").grid(row=4, column=0, sticky=tk.W)
        tk.Spinbox(aircraft_frame, from_=0, to=100).grid(row=4, column=1)
        tk.Label(aircraft_frame, text=str_w).grid(row=4, column=2, sticky=tk.W)
        tk.Label(aircraft_frame, textvariable=self.hangar_armor_weight_var).grid(row=4, column=3)
        tk.Label(aircraft_frame, text="総基数").grid(row=5, column=0, sticky=tk.W)
        tk.Label(aircraft_frame, textvariable=self.total_aircraft_count_var).grid(row=5, column=1)

        return aircraft_frame
    #カタパルト
    def create_catapult_section(self, parent):
        catapult_frame = tk.LabelFrame(parent, text="射出装置")
        tk.Label(catapult_frame, text="種類").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(catapult_frame, values=["Type A", "Type B", "Type C"]).grid(row=0, column=1)
        tree_frame = tk.Frame(catapult_frame)
        tree_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("位置", "種類", str_w), show="headings", height=10)
        details_list.heading("位置", text="位置")
        details_list.heading("種類", text="種類")
        details_list.heading(str_w, text=str_w)
        details_list.column("位置", width=100)
        details_list.column("種類", width=100)
        details_list.column(str_w, width=100)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Button(catapult_frame, text=st_a, command=lambda: self.add_to_catapult(details_list)).grid(row=2, column=0, pady=5)
        tk.Button(catapult_frame, text="削除", command=lambda: self.delete_from_catapult(details_list)).grid(row=2, column=1, pady=5)
        tk.Button(catapult_frame, text="全削除", command=lambda: self.delete_all_from_catapult(details_list)).grid(row=2, column=2, pady=5)

        return catapult_frame
    #カタパルト追加
    def add_to_catapult(self, tree):
        # Add placeholder data: Change as needed for actual functionality
        tree.insert("", "end", values=("位置1", "Type A", "重量100"))
    #カタパルト削除
    def delete_from_catapult(self, tree):
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item)
    #カタパルト全削除
    def delete_all_from_catapult(self, tree):
        for item in tree.get_children():
            tree.delete(item)
    #ミサイルセクション
    def create_missile_section(self, parent):
        missile_frame = tk.LabelFrame(parent, text="ミサイル")

        tk.Label(missile_frame, text="種類").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(missile_frame, values=["Surface-to-Air", "Anti-Ship", "Cruise Missile"]).grid(row=0, column=1)

        tree_frame = tk.Frame(missile_frame)
        tree_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky=tk.NSEW)

        details_list = ttk.Treeview(tree_frame, columns=("位置", "種類", str_w), show="headings", height=10)
        details_list.heading("位置", text="位置")
        details_list.heading("種類", text="種類")
        details_list.heading(str_w, text=str_w)
        details_list.column("位置", width=100)
        details_list.column("種類", width=100)
        details_list.column(str_w, width=100)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Button(missile_frame, text=st_a, command=lambda: self.add_to_missile(details_list)).grid(row=2, column=0, pady=5)
        tk.Button(missile_frame, text="削除", command=lambda: self.delete_from_missile(details_list)).grid(row=2, column=1, pady=5)
        tk.Button(missile_frame, text="全削除", command=lambda: self.delete_all_from_missile(details_list)).grid(row=2, column=2, pady=5)

        return missile_frame
    #ミサイル追加
    def add_to_missile(self, tree):
        # Add placeholder data: Change as needed for actual functionality
        tree.insert("", "end", values=("位置1", "Surface-to-Air", "重量100"))
    #ミサイル削除
    def delete_from_missile(self, tree):
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item)
    #ミサイル全削除
    def delete_all_from_missile(self, tree):
        for item in tree.get_children():
            tree.delete(item)
    #イラスト編集
    def create_graphics_tab(self, parent):
        # Create a frame to hold the sections
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create sections for Trapezoid, Rectangle, Triangle, and Circle
        self.create_trapezoid_section(frame).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.create_triangle_section(frame).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.create_circle_section(frame).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Configure grid to expand properly
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
    #色
    def set_color(self, r_spinbox, g_spinbox, b_spinbox, r, g, b):
        r_spinbox.delete(0, tk.END)
        r_spinbox.insert(0, r)
        g_spinbox.delete(0, tk.END)
        g_spinbox.insert(0, g)
        b_spinbox.delete(0, tk.END)
        b_spinbox.insert(0, b)
    #台形
    def create_trapezoid_section(self, parent):
        trapezoid_frame = tk.LabelFrame(parent, text="台形")


        # 上辺, 下辺, 高さ
        tk.Label(trapezoid_frame, text="上辺").grid(row=0, column=0, sticky=tk.W)
        top_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
        top_spinbox.grid(row=0, column=1)
        tk.Label(trapezoid_frame, text="下辺").grid(row=0, column=2, sticky=tk.W)
        bottom_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
        bottom_spinbox.grid(row=0, column=3)
        tk.Label(trapezoid_frame, text="高さ").grid(row=0, column=4, sticky=tk.W)
        height_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
        height_spinbox.grid(row=0, column=5)

        # 位置
        tk.Label(trapezoid_frame, text="位置 X").grid(row=1, column=0, sticky=tk.W)
        x_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
        x_spinbox.grid(row=1, column=1)
        tk.Label(trapezoid_frame, text="位置 Y").grid(row=1, column=2, sticky=tk.W)
        y_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=1000)
        y_spinbox.grid(row=1, column=3)

        # RGB
        tk.Label(trapezoid_frame, text="RGB").grid(row=2, column=0, sticky=tk.W)
        r_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=255)
        r_spinbox.grid(row=2, column=1)
        g_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=255)
        g_spinbox.grid(row=2, column=2)
        b_spinbox = tk.Spinbox(trapezoid_frame, from_=0, to=255)
        b_spinbox.grid(row=2, column=3)
        color_picker_frame = tk.Frame(trapezoid_frame)
        color_picker_frame.grid(row=2, column=4, columnspan=2)
        red_btn = tk.Button(color_picker_frame, text="赤", bg="red", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 255, 0, 0))
        red_btn.grid(row=0, column=0)
        green_btn = tk.Button(color_picker_frame, text="緑", bg="green", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 0, 255, 0))
        green_btn.grid(row=0, column=1)
        blue_btn = tk.Button(color_picker_frame, text="青", bg="blue", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 0, 0, 255))
        blue_btn.grid(row=0, column=2)
        white_btn = tk.Button(color_picker_frame, text="白", bg="white", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 255, 255, 255))
        white_btn.grid(row=0, column=3)
        black_btn = tk.Button(color_picker_frame, text="黒", bg="black", fg="white", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 0, 0, 0))
        black_btn.grid(row=0, column=4)
        wood_btn = tk.Button(color_picker_frame, text="木", bg="#8B4513", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 139, 69, 19))
        wood_btn.grid(row=1, column=0)
        steel_btn = tk.Button(color_picker_frame, text="鋼", bg="#808080", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 128, 128, 128))
        steel_btn.grid(row=1, column=1)
        gold_btn = tk.Button(color_picker_frame, text="金", bg="#FFD700", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 255, 215, 0))
        gold_btn.grid(row=1, column=2)
        silver_btn = tk.Button(color_picker_frame, text="銀", bg="#C0C0C0", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 192, 192, 192))
        silver_btn.grid(row=1, column=3)
        bronze_btn = tk.Button(color_picker_frame, text="銅", bg="#CD7F32", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 205, 127, 50))
        bronze_btn.grid(row=1, column=4)
        kanpan_btn = tk.Button(color_picker_frame, text="木甲板", bg="#deb887", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 222, 184, 135))
        kanpan_btn.grid(row=2, column=0)
        kurocha_btn = tk.Button(color_picker_frame, text="黒茶", bg="#a0522d", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 160, 82, 45))
        kurocha_btn.grid(row=2, column=1)
        gray_btn = tk.Button(color_picker_frame, text="灰", bg="#696969", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 105, 105, 105))
        gray_btn.grid(row=2, column=2)
        darkgray_btn = tk.Button(color_picker_frame, text="暗灰", bg="#cccccc", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 204, 204, 204))
        darkgray_btn.grid(row=2, column=3)
        darkdarkgray_btn = tk.Button(color_picker_frame, text="黒暗灰", bg="#4f4f4f", command=lambda: self.set_color(r_spinbox, g_spinbox, b_spinbox, 79, 79, 79))
        darkdarkgray_btn.grid(row=2, column=4)
        # 周りの線ありチェックボックス
        border_var = tk.BooleanVar()
        tk.Checkbutton(trapezoid_frame, text="ふち線あり", variable=border_var).grid(row=3, column=0, columnspan=2, sticky=tk.W)


        # 追加ボタン
        def add_trapezoid():
            try:
                top = int(top_spinbox.get())
                bottom = int(bottom_spinbox.get())
                height = int(height_spinbox.get())
                x = int(x_spinbox.get())
                y = int(y_spinbox.get())
                r = int(r_spinbox.get())
                g = int(g_spinbox.get())
                b = int(b_spinbox.get())
                border_r = 0
                border_g = 0
                border_b = 0
            except ValueError:
                messagebox.showwarning("警告", "すべての値を入力してください。")
                return

            if any(v == "" for v in [top, bottom, height, x, y, r, g, b]):
                messagebox.showwarning("警告", "すべての値を入力してください。")
                return

            trapezoid = {
                "top": top,
                "bottom": bottom,
                "height": height,
                "x": x,
                "y": y,
                "color": (r, g, b),
                "border": border_var.get(),
                "border_color": (border_r, border_g, border_b)
            }
            self.trapezoids.append(trapezoid)
            details_list.insert("", "end", values=(x, y, len(self.trapezoids) - 1))
            self.draw_trapezoid(trapezoid)

        tk.Button(trapezoid_frame, text="追加", command=add_trapezoid).grid(row=4, column=0, pady=5)

        # リスト
        tree_frame = tk.Frame(trapezoid_frame)
        tree_frame.grid(row=5, column=0, columnspan=6, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("位置X", "位置Y", "ID"), show="headings", height=10)
        details_list.heading("位置X", text="位置X")
        details_list.heading("位置Y", text="位置Y")
        details_list.heading("ID", text="ID")
        details_list.column("位置X", width=100)
        details_list.column("位置Y", width=100)
        details_list.column("ID", width=100)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 削除ボタン, リセットボタン
        def delete_trapezoid():
            selected_item = details_list.selection()
            if selected_item:
                item_id = details_list.item(selected_item)["values"][2]
                del self.trapezoids[item_id]
                details_list.delete(selected_item)
                self.update_lines()

        tk.Button(trapezoid_frame, text="削除", command=delete_trapezoid).grid(row=7, column=0, pady=5)
        tk.Button(trapezoid_frame, text="リセット").grid(row=7, column=1, pady=5)

        def on_right_click(event):
            item = details_list.identify_row(event.y)
            if item:
                details_list.selection_set(item)
                delete_trapezoid()
            self.update_lines()

        def reset_triangles():
            self.triangles.clear()
            for item in details_list.get_children():
                details_list.delete(item)
            self.update_lines()


        details_list.bind("<Button-3>", on_right_click)

        return trapezoid_frame
    #台形描画
    def draw_trapezoid(self, trapezoid):
        canvas_center_x = self.graphics_canvas.winfo_width() // 2
        canvas_center_y = self.graphics_canvas.winfo_height() // 2

        top = trapezoid["top"] * self.zoom_scale
        bottom = trapezoid["bottom"] * self.zoom_scale
        height = trapezoid["height"] * self.zoom_scale
        x = trapezoid["x"] * self.zoom_scale
        y = trapezoid["y"] * self.zoom_scale
        color = "#{:02x}{:02x}{:02x}".format(*trapezoid["color"])

        # 上辺と下辺の左右の端の座標を計算
        top_left_x = canvas_center_x + x - top // 2
        top_right_x = canvas_center_x + x + top // 2
        bottom_left_x = canvas_center_x + x - bottom // 2
        bottom_right_x = canvas_center_x + x + bottom // 2

        top_y = canvas_center_y + y - height // 2
        bottom_y = canvas_center_y + y + height // 2

        # 上から下まで一定の間隔で横線を引く
        num_lines = int(height)  # 線の数（高さの整数部分を基準）
        for i in range(num_lines + 1):
            line_y = top_y + i * (height / num_lines)
            # 線の左右の座標を線形補完で求める
            line_left_x = top_left_x + i * (bottom_left_x - top_left_x) / num_lines
            line_right_x = top_right_x + i * (bottom_right_x - top_right_x) / num_lines
            self.graphics_canvas.create_line(line_left_x, line_y, line_right_x, line_y, fill=color)

        # 境界線の描画
        if trapezoid["border"]:
            border_color = "#{:02x}{:02x}{:02x}".format(*trapezoid["border_color"])
            # 上辺、右辺、下辺、左辺の順で境界線を描画
            self.graphics_canvas.create_line(top_left_x, top_y, top_right_x, top_y, fill=border_color)
            self.graphics_canvas.create_line(top_right_x, top_y, bottom_right_x, bottom_y, fill=border_color)
            self.graphics_canvas.create_line(bottom_right_x, bottom_y, bottom_left_x, bottom_y, fill=border_color)
            self.graphics_canvas.create_line(bottom_left_x, bottom_y, top_left_x, top_y, fill=border_color)
    #三角形
    def create_triangle_section(self, parent):
        triangle_frame = tk.LabelFrame(parent, text="三角")

        # 底辺, 頂点X, 高さ
        tk.Label(triangle_frame, text="底辺").grid(row=0, column=0, sticky=tk.W)
        base_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
        base_spinbox.grid(row=0, column=1)
        tk.Label(triangle_frame, text="頂点X").grid(row=0, column=2, sticky=tk.W)
        apex_x_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
        apex_x_spinbox.grid(row=0, column=3)
        tk.Label(triangle_frame, text="高さ").grid(row=0, column=4, sticky=tk.W)
        height_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
        height_spinbox.grid(row=0, column=5)

        # 位置
        tk.Label(triangle_frame, text="位置 X").grid(row=1, column=0, sticky=tk.W)
        x_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
        x_spinbox.grid(row=1, column=1)
        tk.Label(triangle_frame, text="位置 Y").grid(row=1, column=2, sticky=tk.W)
        y_spinbox = tk.Spinbox(triangle_frame, from_=0, to=1000)
        y_spinbox.grid(row=1, column=3)

        # RGB
        tk.Label(triangle_frame, text="RGB").grid(row=2, column=0, sticky=tk.W)
        r_spinbox = tk.Spinbox(triangle_frame, from_=0, to=255)
        r_spinbox.grid(row=2, column=1)
        g_spinbox = tk.Spinbox(triangle_frame, from_=0, to=255)
        g_spinbox.grid(row=2, column=2)
        b_spinbox = tk.Spinbox(triangle_frame, from_=0, to=255)
        b_spinbox.grid(row=2, column=3)

        # 周りの線ありチェックボックス
        border_var = tk.BooleanVar()
        tk.Checkbutton(triangle_frame, text="ふち線あり", variable=border_var).grid(row=3, column=0, columnspan=2, sticky=tk.W)

        # 追加ボタン
        def add_triangle():
            try:
                base = int(base_spinbox.get())
                apex_x = int(apex_x_spinbox.get())
                height = int(height_spinbox.get())
                x = int(x_spinbox.get())
                y = int(y_spinbox.get())
                r = int(r_spinbox.get())
                g = int(g_spinbox.get())
                b = int(b_spinbox.get())
                border_r = 0
                border_g = 0
                border_b = 0
                if border_var.get():
                    border_r = 0  # Set border color as needed
                    border_g = 0
                    border_b = 0
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid numbers.")
                return

            # Calculate the coordinates of the triangle
            triangle = {
                "base": base,
                "apex_x": apex_x,
                "height": height,
                "x": x,
                "y": y,
                "color": (r, g, b),
                "border": border_var.get(),
                "border_color": (border_r, border_g, border_b)
            }

            self.triangles.append(triangle)

            # Add the triangle details to the list
            details_list.insert("", "end", values=(x, y, f"Triangle {len(details_list.get_children()) + 1}"))
            self.draw_triangle(triangle)

        tk.Button(triangle_frame, text="追加", command=add_triangle).grid(row=4, column=0, pady=5)

        # リスト
        tree_frame = tk.Frame(triangle_frame)
        tree_frame.grid(row=5, column=0, columnspan=6, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("位置X", "位置Y", "ID"), show="headings", height=10)
        details_list.heading("位置X", text="位置X")
        details_list.heading("位置Y", text="位置Y")
        details_list.heading("ID", text="ID")
        details_list.column("位置X", width=100)
        details_list.column("位置Y", width=100)
        details_list.column("ID", width=100)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 削除ボタン, リセットボタン
        def delete_triangle():
            selected_item = details_list.selection()
            if selected_item:
                details_list.delete(selected_item)
            self.update_lines()

        tk.Button(triangle_frame, text="削除", command=delete_triangle).grid(row=7, column=0, pady=5)
        tk.Button(triangle_frame, text="リセット").grid(row=7, column=1, pady=5)
        def on_right_click(event):
            item = details_list.identify_row(event.y)
            if item:
                details_list.selection_set(item)
                delete_triangle()
            self.update_lines()

        def reset_triangles():
            details_list.delete(*details_list.get_children())
            self.triangles.clear()
            for item in details_list.get_children():
                details_list.delete(item)
            self.update_lines()
        details_list.bind("<Button-3>", on_right_click)

        return triangle_frame
    #三角形描画
    def draw_triangle(self, triangle):
        canvas_center_x = self.graphics_canvas.winfo_width() // 2
        canvas_center_y = self.graphics_canvas.winfo_height() // 2

        base = triangle["base"] * self.zoom_scale
        apex_x = triangle["apex_x"] * self.zoom_scale
        height = triangle["height"] * self.zoom_scale
        x = triangle["x"] * self.zoom_scale
        y = triangle["y"] * self.zoom_scale
        color = "#{:02x}{:02x}{:02x}".format(*triangle["color"])

        # 底辺の左右の座標を計算
        bottom_left_x = canvas_center_x + x
        bottom_right_x = canvas_center_x + x + base
        apex_y = canvas_center_y + y
        bottom_y = canvas_center_y + y + height

        # 一定の間隔で横線を引くための線の本数
        num_lines = int(height)  # 高さの整数部分に基づいて線の本数を決定
        for i in range(num_lines + 1):
            line_y = apex_y + i * (bottom_y - apex_y) / num_lines
            # 左右の座標を線形補完で計算
            line_left_x = apex_x + (bottom_left_x - apex_x) * (i / num_lines)
            line_right_x = apex_x + (bottom_right_x - apex_x) * (i / num_lines)
            self.graphics_canvas.create_line(line_left_x, line_y, line_right_x, line_y, fill=color)

        # 境界線の描画
        if triangle["border"]:
            border_color = "#{:02x}{:02x}{:02x}".format(*triangle["border_color"])
            # 底辺と左右の辺を線で描画
            self.graphics_canvas.create_line(bottom_left_x, bottom_y, bottom_right_x, bottom_y, fill=border_color)  # 底辺
            self.graphics_canvas.create_line(bottom_left_x, bottom_y, canvas_center_x + x + apex_x, apex_y, fill=border_color)  # 左の辺
            self.graphics_canvas.create_line(bottom_right_x, bottom_y, canvas_center_x + x + apex_x, apex_y, fill=border_color)  # 右の辺
    #円
    def create_circle_section(self, parent):
        circle_frame = tk.LabelFrame(parent, text="円")

        # 横半径, 縦半径
        tk.Label(circle_frame, text="横半径").grid(row=0, column=0, sticky=tk.W)
        horizontal_radius_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
        horizontal_radius_spinbox.grid(row=0, column=1)
        tk.Label(circle_frame, text="縦半径").grid(row=1, column=0, sticky=tk.W)
        vertical_radius_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
        vertical_radius_spinbox.grid(row=1, column=1)

        # 位置
        tk.Label(circle_frame, text="中心 X").grid(row=2, column=0, sticky=tk.W)
        x_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
        x_spinbox.grid(row=2, column=1)
        tk.Label(circle_frame, text="中心 Y").grid(row=3, column=0, sticky=tk.W)
        y_spinbox = tk.Spinbox(circle_frame, from_=0, to=1000)
        y_spinbox.grid(row=3, column=1)

        # RGB
        tk.Label(circle_frame, text="RGB").grid(row=4, column=0, sticky=tk.W)
        tk.Label(circle_frame, text="R").grid(row=5, column=0, sticky=tk.W)
        r_spinbox = tk.Spinbox(circle_frame, from_=0, to=255)
        r_spinbox.grid(row=5, column=1)
        tk.Label(circle_frame, text="G").grid(row=6, column=0, sticky=tk.W)
        g_spinbox = tk.Spinbox(circle_frame, from_=0, to=255)
        g_spinbox.grid(row=6, column=1)
        tk.Label(circle_frame, text="B").grid(row=7, column=0, sticky=tk.W)
        b_spinbox = tk.Spinbox(circle_frame, from_=0, to=255)
        b_spinbox.grid(row=7, column=1)

        # 周りの線ありチェックボックス
        border_var = tk.BooleanVar()
        tk.Checkbutton(circle_frame, text="ふち線あり", variable=border_var).grid(row=8, column=0, columnspan=2, sticky=tk.W)

        # 追加ボタン
        def add_circle():
            try:
                horizontal_radius = int(horizontal_radius_spinbox.get())
                vertical_radius = int(vertical_radius_spinbox.get())
                x = int(x_spinbox.get())
                y = int(y_spinbox.get())
                r = int(r_spinbox.get())
                g = int(g_spinbox.get())
                b = int(b_spinbox.get())
                border_r = 0
                border_g = 0
                border_b = 0
                if border_var.get():
                    border_r = r
                    border_g = g
                    border_b = b
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid numbers.")
                return

            # Add the circle details to the list
            details_list.insert("", "end", values=(x, y, f"Circle {len(details_list.get_children()) + 1}"))
            circle = {
                "horizontal_radius": horizontal_radius,
                "vertical_radius": vertical_radius,
                "x": x,
                "y": y,
                "color": (r, g, b),
                "border": border_var.get(),
                "border_color": (border_r, border_g, border_b)
            }
            self.circles.append(circle)
            self.draw_circle(circle)

        tk.Button(circle_frame, text="追加", command=add_circle).grid(row=9, column=0, pady=5)


        # リスト
        tree_frame = tk.Frame(circle_frame)
        tree_frame.grid(row=10, column=0, columnspan=6, pady=5, sticky=tk.NSEW)
        details_list = ttk.Treeview(tree_frame, columns=("位置X", "位置Y", "ID"), show="headings", height=10)
        details_list.heading("位置X", text="位置X")
        details_list.heading("位置Y", text="位置Y")
        details_list.heading("ID", text="ID")
        details_list.column("位置X", width=100)
        details_list.column("位置Y", width=100)
        details_list.column("ID", width=100)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=details_list.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=details_list.xview)
        details_list.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        details_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 削除ボタン, リセットボタン
        def delete_circle():
            selected_item = details_list.selection()
            if selected_item:
                details_list.delete(selected_item)
            self.update_lines()

        def reset_circles():
            self.circles.clear()
            for item in details_list.get_children():
                details_list.delete(item)
            self.update_lines()

        tk.Button(circle_frame, text="削除", command=delete_circle).grid(row=11, column=0, pady=5)
        tk.Button(circle_frame, text="リセット", command=reset_circles).grid(row=11, column=1, pady=5)

        def on_right_click(event):
            item = details_list.identify_row(event.y)
            if item:
                details_list.selection_set(item)
                delete_circle()
            self.update_lines()



        details_list.bind("<Button-3>", on_right_click)

        return circle_frame
    #円描画
    def draw_circle(self, circle):
        # データの設定
        canvas_center_x = self.graphics_canvas.winfo_width() // 2
        canvas_center_y = self.graphics_canvas.winfo_height() // 2

        horizontal_radius = circle["horizontal_radius"] * self.zoom_scale
        vertical_radius = circle["vertical_radius"] * self.zoom_scale
        x = circle["x"] * self.zoom_scale
        y = circle["y"] * self.zoom_scale
        color = "#{:02x}{:02x}{:02x}".format(*circle["color"])

        # 楕円の境界ボックスの計算
        left = canvas_center_x + x - horizontal_radius
        right = canvas_center_x + x + horizontal_radius
        top = canvas_center_y + y - vertical_radius
        bottom = canvas_center_y + y + vertical_radius

        # 楕円を描くために上から下へ横線を描画
        num_lines = int(vertical_radius * 2)  # 楕円の高さに基づいて線の本数を決定
        for i in range(num_lines + 1):
            # 各横線のY座標を計算
            line_y = top + i * (bottom - top) / num_lines
            # 楕円の左右のX座標を楕円の方程式から計算
            normalized_y = (line_y - canvas_center_y - y) / vertical_radius  # 正規化されたY座標
            if abs(normalized_y) <= 1:  # 楕円の範囲内であることを確認
                line_half_width = horizontal_radius * (1 - normalized_y ** 2) ** 0.5
                line_left_x = canvas_center_x + x - line_half_width
                line_right_x = canvas_center_x + x + line_half_width

                if i == 0 or i == num_lines:
                    # 上端または下端の線はそのまま描画
                    self.graphics_canvas.create_line(line_left_x, line_y, line_right_x, line_y, fill="black")
                else:
                    # 通常の線は、左右1pxずつ黒、中央は指定された色で描画
                    self.graphics_canvas.create_line(line_left_x, line_y, line_left_x + 1, line_y, fill="black")
                    self.graphics_canvas.create_line(line_left_x + 1, line_y, line_right_x - 2, line_y, fill=color)
                    self.graphics_canvas.create_line(line_right_x - 2, line_y, line_right_x, line_y, fill="black")


# アプリケーションの実行
if __name__ == "__main__":
    app = ShipDesignerApp()
    app.mainloop()

