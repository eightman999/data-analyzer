import json
import tkinter as tk

# JSONデータをファイルから読み込む
try:
    with open('output.json', 'r') as file:
        raw_data = json.load(file)

        # JSONが辞書型で"line_graphic"キーがあることを確認して処理
        if isinstance(raw_data, dict) and "line_graphic" in raw_data:
            raw_data = raw_data["line_graphic"]

        # 各データが辞書型か確認し、適切に処理
        line_graphic = [
            {
                "x1": float(data.get("x1", 0)),
                "y1": float(data.get("y1", 0)),
                "x2": float(data.get("x2", 0)),
                "y2": float(data.get("y2", 0)),
                "color": data.get("color", "#000000"),
                "border": str(data.get("border", "false")).lower() == "true"
            }
            for data in raw_data if isinstance(data, dict)
        ]
except FileNotFoundError:
    print("Error: 'output.json' file not found.")
    line_graphic = []
except json.JSONDecodeError:
    print("Error: Failed to parse JSON data.")
    line_graphic = []


class LineViewerApp:
    def __init__(self, root, width=800, height=600):
        self.root = root
        self.canvas_width = width
        self.canvas_height = height
        self.zoom_factor = 1.0

        # メインフレーム作成
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas作成
        self.canvas = tk.Canvas(
            self.main_frame, width=self.canvas_width, height=self.canvas_height, bg="white"
        )
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ボタンエリア作成
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # ズームイン・アウトボタン作成
        zoom_in_button = tk.Button(self.button_frame, text="Zoom In", command=self.zoom_in)
        zoom_in_button.pack(side=tk.LEFT, padx=5, pady=5)

        zoom_out_button = tk.Button(self.button_frame, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.pack(side=tk.LEFT, padx=5, pady=5)

        # 初期描画
        self.draw()

    def draw(self):
        """Canvas上に図形を描画"""
        self.canvas.delete("all")  # 再描画時にクリア
        cx, cy = self.canvas_width // 2, self.canvas_height // 2

        for data in line_graphic:
            # 各点をキャンバス中心にオフセットし、ズーム計算を反映
            x1 = cx + data["x1"] * self.zoom_factor
            y1 = cy - data["y1"] * self.zoom_factor  # Y軸は反転
            x2 = cx + data["x2"] * self.zoom_factor
            y2 = cy - data["y2"] * self.zoom_factor  # Y軸は反転
            color = data.get("color", "#000000")
            border = data.get("border", False)

            # 線を描画
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, capstyle=tk.BUTT)

            # 境界線が指定されている場合
            if border:
                self.canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=color)
                self.canvas.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill=color)

    def zoom_in(self):
        """ズームイン処理"""
        self.zoom_factor *= 1.2  # ズーム倍率を上げる
        self.draw()  # 再描画

    def zoom_out(self):
        """ズームアウト処理"""
        self.zoom_factor *= 0.8  # ズーム倍率を下げる
        self.draw()  # 再描画


# メイン処理
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Line Graphic Viewer with Zoom")

    # アプリケーション起動
    app = LineViewerApp(root, width=800, height=600)

    root.mainloop()
