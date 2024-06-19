from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sys
from view.Main_ui import Ui_MainWindow

class Root(QMainWindow):
    def __init__(self):
        super().__init__()
        # Placeholder central widget
        self.ui  = Ui_MainWindow()
        self.ui.setupUi(self)

    def show(self):
        print("showing the main window")
        super().show()