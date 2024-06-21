from PySide6.QtWidgets import QMainWindow
from view.Main_ui import Ui_MainWindow
import images.qresources_rc

class Root(QMainWindow):
    def __init__(self):
        super().__init__()
        # Placeholder central widget
        self.ui  = Ui_MainWindow()
        self.ui.setupUi(self)
        images.qresources_rc.qInitResources()
        print("resources loaded")

    def show(self):
        print("showing the main window")
        super().show()

    def tweat_UI(self) -> None:
        pass
        # self.ui.