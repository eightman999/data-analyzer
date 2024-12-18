import os
from tkinter import Tk, filedialog
from PIL import Image

def convert_png_to_dds(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            png_path = os.path.join(directory, filename)
            dds_path = os.path.splitext(png_path)[0] + ".dds"
            with Image.open(png_path) as img:
                img.save(dds_path, format='DDS')
            print(f"Converted {png_path} to {dds_path}")

def main():
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Directory with PNG Files")
    if directory:
        convert_png_to_dds(directory)
    else:
        print("No directory selected")

if __name__ == "__main__":
    main()