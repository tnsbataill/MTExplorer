from tkinter import Tk
from tkinter import ttk

class Root(Tk):
    def __init__(self):
        super().__init__()

        start_width = 1400
        min_width = 400
        start_height = 600
        min_height = 250
        style = ttk.Style(self)
        style.theme_use('clam')
        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title("BomBrowser 2024")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
