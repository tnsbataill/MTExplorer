"""main controller class"""

from model.main import Model
from view.main import View
import sys

from controller.bombroswerqt import BomBrowserController

class Controller:
    "Main controller Class"
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.bom_browser_controller = BomBrowserController(model, view)

        self.model.bom.add_event_listener("bom_changed", self.bom_changed_listener)
        self.model.boms.add_event_listener("boms_changed", self.filter_changed_listener)

    def bom_changed_listener(self, *args) -> None:
        """action for change of selected bom in boms"""
        self.bom_browser_controller.bom_refresh()

    def filter_changed_listener(self, *args) -> None:
        """action for change of BOMs model list"""
        self.bom_browser_controller.boms_refresh()

    def start(self) -> None:
        """Initiation of program loop"""
        self.view.show()


