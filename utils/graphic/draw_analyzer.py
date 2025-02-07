import cv2
import numpy as np
import json

def detect_lines(image_path, pixel_scale=1, origin_x=0, origin_y=0):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image.shape[2] == 4:  # Check if image has alpha channel
        alpha_channel = image[:, :, 3]
        image = image[:, :, :3]
    else:
        alpha_channel = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8) * 255

    height, width, _ = image.shape

    line_segments = []
    for y in range(0, height, pixel_scale):
        row = image[y, :]
        alpha_row = alpha_channel[y, :]
        inside_line = False
        x1 = None
        for x in range(width):
            alpha = alpha_row[x]
            if alpha > 0:  # Accept all non-transparent pixels, including white
                if not inside_line:
                    x1 = x
                    inside_line = True
            else:
                if inside_line:
                    x2 = x - 1
                    color = image[y, (x1 + x2) // 2].tolist()
                    line_segments.append({
                        "x1": (x1 - origin_x) // pixel_scale,
                        "y1": (y - origin_y) // pixel_scale,
                        "x2": (x2 - origin_x) // pixel_scale,
                        "y2": (y - origin_y) // pixel_scale,
                        "color": f"#{color[2]:02x}{color[1]:02x}{color[0]:02x}",
                        "border": "true",
                    })
                    inside_line = False

    return line_segments

def save_to_json(lines, output_path):
    data = {"line_graphic": lines}
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    image_path = "input.png"
    output_path = "output.json"
    pixel_scale = 1  # Example: Treat 4x4 pixels as 1 logical pixel
    origin_x = 632  # Specify the reference point X
    origin_y = 1283  # Specify the reference point Y
    lines = detect_lines(image_path, pixel_scale, origin_x, origin_y)
    save_to_json(lines, output_path)
    print("Line extraction complete. JSON saved.")
