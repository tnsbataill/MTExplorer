"""general view setup"""
from view.root import Root
from view.Main_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication

class View:
    """initialize general view class"""
    def __init__(self):
        self.root = Root()

    def show(self):
        self.root.show()