import cv2
import svgwrite
from PIL import Image


def png_to_svg_with_color(input_path, output_path):
    # カラー画像を読み込む
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("入力ファイルが見つかりません")

    # 画像サイズを取得
    height, width, _ = image.shape

    # SVGファイルの初期化
    dwg = svgwrite.Drawing(output_path, profile='tiny', size=(width, height))

    # 各ピクセルを走査して色付きの長方形をSVGに追加
    for y in range(height):
        for x in range(width):
            # ピクセルの色情報（BGR）
            b, g, r = image[y, x]

            # 非白色ピクセルのみを描画 (オプション)
            if (r, g, b) != (255, 255, 255):  # 白以外を処理
                color_hex = f"#{r:02x}{g:02x}{b:02x}"  # RGBをHEXに変換
                dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill=color_hex))  # 小文字の`rect`

    # SVG書き出し
    dwg.save()
    print(f"SVGファイルが生成されました: {output_path}")
