"""Python version of BOM Browser. Designed such that adding/adjusting 
    features in the future should be doable for someone with 
    python knowledge."""

import sys
from model.main import Model
from view.main import View
from controller.main import Controller
from utils.startup import startup
from PySide6.QtWidgets import QApplication


def main():
    """Main class to get the application rolling"""

    startup()
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    model = Model()
    view = View()
    controller = Controller(model, view)
    model.boms.load_boms()
    controller.start()

    view.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()