import os
from tkinter import Tk, filedialog
from PIL import Image

def convert_png_to_dds(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            png_path = os.path.join(directory, filename)
            dds_path = os.path.splitext(png_path)[0] + ".dds"
            with Image.open(png_path) as img:
                print(f"{png_path} mode: {img.mode}")
                img.save(dds_path, format='DDS')
            print(f"Converted {png_path} to {dds_path}")
def convert_dds_to_png(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".dds"):
            dds_path = os.path.join(directory, filename)
            png_path = os.path.splitext(dds_path)[0] + ".png"
            with Image.open(dds_path) as img:
                img.save(png_path, format='PNG')
            print(f"Converted {dds_path} to {png_path}")

def main():
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Directory with Image Files")
    if directory:
        choice = input("Convert (1) PNG to DDS or (2) DDS to PNG? Enter 1 or 2: ")
        if choice == '1':
            convert_png_to_dds(directory)
        elif choice == '2':
            convert_dds_to_png(directory)
        else:
            print("Invalid choice")
    else:
        print("No directory selected")

if __name__ == "__main__":
    main()