import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Hide Tkinter main window
Tk().withdraw()

# Ask user to select a directory
input_dir = askdirectory(title="Select directory")

# Define the output directory
output_dir = 'database/FLAGS'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over files in the selected directory
for filename in os.listdir(input_dir):
    # Check if the file has a .tga extension and the name is exactly three characters long
    if filename.endswith('.tga') and len(filename) == 7:  # 3 chars + '.tga' = 7 chars
        # Construct full file paths
        src_file = os.path.join(input_dir, filename)
        dest_file = os.path.join(output_dir, filename)
        # Copy the file to the output directory
        shutil.copy(src_file, dest_file)

print(f"Files copied to {output_dir}")