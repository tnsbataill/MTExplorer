"""Python version of BOM Browser. Designed such that adding/adjusting 
    features in the future should be doable for someone with 
    python knowledge."""

from model.main import Model
from view.main import View
from controller.main import Controller
from utils.startup import startup

def main():
    """Main class to get the application rolling"""

    startup()
    model = Model()
    view = View()
    controller = Controller(model, view)
    model.boms.load_boms()
    controller.start()

if __name__ == "__main__":
    main()
