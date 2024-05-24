"""BOMs model setup"""
import os
import pandas as pd
from model.base import ObservableModel
from model.sql import get_datatable
import utils.strings



class Boms(ObservableModel):
    """BOMs model class definition"""
    def __init__(self):
        super().__init__()
        self.home_dir: str = os.path.expanduser("~")
        self.bomslistbase: pd.DataFrame = None
        self.bomslist: pd.DataFrame = self.bomslistbase
        self.selected_bom: str = None
        self.currentfilter: str = None

    def load_boms(self) -> None:
        #self.load_boms_list_csv()
        self.load_boms_list_sql()

    def load_boms_list_sql(self) -> None:
        """load procedure for boms list"""
        self.bomslistbase = get_datatable(self, utils.strings.BOMS_SQL_STRING)
        if self.bomslistbase is not None:
            self.bomslist = self.bomslistbase
            self.trigger_event("boms_changed")
            save_path = [self.home_dir, utils.strings.BOMS_PKL_PATH]
            self.bomslistbase.to_pickle(''.join(save_path), 'infer')

    def load_boms_list_csv(self) -> None:
        """load local csv of boms list"""
        try:
            self.bomslistbase =  pd.read_pickle(self.home_dir + utils.strings.BOMS_PKL_PATH)
        except PermissionError:
            print("Pickle file open permission denied...")

        else:
            self.bomslist = self.bomslistbase
            self.trigger_event("boms_changed")

    def search_string(self, s, search):
        """Helper function to search for given string"""
        return search in str(s).lower()

    def boms_filter(self, filter_input_str) -> None:
        """BOMs search filtering function"""
        if filter_input_str and self.bomslistbase is not None:
            mask = self.bomslistbase.apply(lambda x: x.map(
                lambda s:self.search_string(s, filter_input_str)))
            self.bomslist = self.bomslistbase.loc[mask.any(axis=1)]
        else:
            self.bomslist = self.bomslistbase
        self.trigger_event("boms_changed")

    def boms_sort(self, sort_string) -> None:
        """Sort function accepts string of dataframe column name"""
        if self.bomslist is not None:
            self.bomslist.sort_values(sort_string)
