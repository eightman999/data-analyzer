
from tkinter import Tk, filedialog

def select_directory():
    root = Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory(title="Select Directory Containing Equipment Files")
    return directory