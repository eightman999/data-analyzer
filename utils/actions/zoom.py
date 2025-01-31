def zoom_in(self):
    self.zoom_scale += 0.2  # ズーム倍率を増加
    self.update_lines()  # 描画を更新
#ZOOM OUT
def zoom_out(self):
    if self.zoom_scale > 2.5:  # ズーム倍率が1より小さくならないように
        self.zoom_scale -= 0.2  # ズーム倍率を減少
    self.update_lines()  # 描画を更新