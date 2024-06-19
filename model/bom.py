"""definition of BOM class"""

from model.base import ObservableModel
from model.sql import get_datatable
from utils.strings import BOM_SQL_STRING_PRE, BOM_SQL_STRING_POST
import pandas as pd

class Bom(ObservableModel):
    """definition of BOM class"""
    def __init__(self):
        super().__init__()
        self.bom_name = None
        # self.bom_list = {}
        self.bom_list = pd.DataFrame()
        self.selected_item = None

    def change(self, targetbom: str) -> None:
        """Change the bom to the one selected from boms_list"""
        self.bom_name = targetbom
        sql_string = BOM_SQL_STRING_PRE + self.bom_name + BOM_SQL_STRING_POST
        self.bom_list = get_datatable(self, sql_string)
        self.bom_list["Checked"] = False
        self.trigger_event("bom_changed")
