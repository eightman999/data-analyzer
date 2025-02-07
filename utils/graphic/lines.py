class Circle:
    def __init__(self, data,x_add,y_add):
        try:
            self.horizontal_radius = float(data.get("horizontal_radius", 0.0))
            self.vertical_radius = float(data.get("vertical_radius", 0.0))
            self.r,self.g,self.b = hex_to_rgb(str(data.get("rgb")))
            self.border = str(data.get("border", "none"))
            self.x = float(data.get("x", 0.0))+float(x_add)
            self.y = float(data.get("y", 0.0))+float(y_add)
            self.border_color = (0,0,0)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid data for Circle: {e}")

    def to_dict(self):
        """
        インスタンスの属性を指定されたフォーマットで辞書として返す。
        """
        return {
            "horizontal_radius": self.horizontal_radius,
            "vertical_radius": self.vertical_radius,
            "x": self.x,
            "y": self.y,
            "color": (self.r, self.g, self.b),  # (r, g, b)形式
            "border": self.border,
            "border_color": self.border_color  # (r, g, b)形式
        }


class Trapezoid:
    def __init__(self, data,x_add,y_add):
        try:
            self.top = float(data.get("top", 0.0))
            self.bottom = float(data.get("bottom", 0.0))
            self.height = float(data.get("height", 0.0))
            self.r,self.g,self.b = hex_to_rgb(str(data.get("rgb")))
            self.border = str(data.get("border", "none"))
            self.x = float(data.get("x", 0.0))+float(x_add)
            self.y = float(data.get("y", 0.0))+float(y_add)
            self.border_color = (0,0,0)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid data for Trapezoid: {e}")

    def to_dict(self):
        """
        インスタンスの属性を指定されたフォーマットで辞書として返す。
        """
        return {
            "top": self.top,
            "bottom": self.bottom,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "color": (self.r,self.g,self.b),  # (r, g, b)形式
            "border": self.border,
            "border_color": self.border_color  # (r, g, b)形式
        }


class Triangle:
    def __init__(self, data,x_add,y_add):
        try:
            self.base = float(data.get("base", 0.0))
            self.apex_x = float(data.get("apex_x", 0.0))
            self.height = float(data.get("height", 0.0))
            self.r,self.g,self.b = hex_to_rgb(str(data.get("rgb")))
            self.border = str(data.get("border", "none"))
            self.x = float(data.get("x", 0.0))+float(x_add)
            self.y = float(data.get("y", 0.0))+float(y_add)
            self.border_color = (0,0,0)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid data for Triangle: {e}")

    def to_dict(self):
        """
        インスタンスの属性を指定されたフォーマットで辞書として返す。
        """
        return {
            "base": self.base,
            "apex_x": self.apex_x,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "color": (self.r,self.g,self.b),  # (r, g, b)形式
            "border": self.border,
            "border_color": self.border_color  # (r, g, b)形式
        }

def hex_to_rgb(hex_color):
    """
    16進数カラーコードをR, G, B (10進数)タプルに変換
    """
    if not isinstance(hex_color, str) or len(hex_color) not in (6, 7) or not hex_color.lstrip('#').isalnum():
        raise ValueError("Invalid hex color format")

    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:  # 有効な6桁カラーコードの処理
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    else:
        raise ValueError("Invalid hex color format")
