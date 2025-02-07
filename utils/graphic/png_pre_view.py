import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk


class ImageZoom(tk.Tk):
    def __init__(self, image_path):
        super().__init__()
        self.title("Zoom In/Out Image with Buttons")

        # Canvasの設定
        self.canvas = Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 元画像の読み込み
        self.original_image = Image.open(image_path)
        self.current_image = self.original_image.copy()
        self.image_scale = 1.0  # 初期スケール値
        self.tk_image = ImageTk.PhotoImage(self.current_image)

        # 画像をCanvasに描画
        self.canvas_image_id = self.canvas.create_image(
            400, 300, image=self.tk_image, anchor=tk.CENTER
        )

        # バインド (マウスホイールでズーム)
        self.canvas.bind("<MouseWheel>", self.zoom_with_wheel)

        # ボタンの追加 (ズームイン/アウト)
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        self.zoom_in_button = tk.Button(self.button_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=10)

        self.zoom_out_button = tk.Button(self.button_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=10)

    def update_image(self):
        """現在のスケールに合わせて画像を更新"""
        width, height = self.original_image.size
        new_size = (int(width * self.image_scale), int(height * self.image_scale))

        # アンチエイリアス無しでリサイズ (ジャギー効果)
        resized_image = self.original_image.resize(new_size, Image.NEAREST)

        # Canvasの画像を更新
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.canvas_image_id, image=self.tk_image)

    def zoom_with_wheel(self, event):
        """マウスホイールによるズームイン/アウト"""
        if event.delta > 0:  # ホイールを上に回す -> ズームイン
            self.image_scale *= 1.1
        elif event.delta < 0:  # ホイールを下に回す -> ズームアウト
            self.image_scale /= 1.1

        self.image_scale = max(0.1, min(self.image_scale, 5.0))
        self.update_image()

    def zoom_in(self):
        """ズームイン (ボタン用)"""
        self.image_scale *= 1.1
        self.image_scale = min(self.image_scale, 5.0)  # 最大スケールを制限
        self.update_image()

    def zoom_out(self):
        """ズームアウト (ボタン用)"""
        self.image_scale /= 1.1
        self.image_scale = max(self.image_scale, 0.1)  # 最小スケールを制限
        self.update_image()


if __name__ == "__main__":
    # 画像ファイルのパス (PNG画像を指定してください)
    image_file_path = "input.png"

    app = ImageZoom(image_file_path)
    app.mainloop()
