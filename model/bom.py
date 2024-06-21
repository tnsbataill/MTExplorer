"""definition of BOM class"""

from model.base import ObservableModel
from model.sql import get_datatable
from utils.strings import BOM_SQL_STRING_PRE_TEST, BOM_SQL_STRING_POST_TEST
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
        sql_string = BOM_SQL_STRING_PRE_TEST + self.bom_name + BOM_SQL_STRING_POST_TEST
        self.bom_list = get_datatable(self, sql_string)

        if self.bom_list is not None:
            self.bom_list["Checked"] = False
        else:
            self.bom_list = pd.DataFrame({"Checked": []})
            
        self.trigger_event("bom_changed")
