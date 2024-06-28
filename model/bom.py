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

        if self.bom_list is not None:
            self.bom_list["Checked"] = False
            self.bom_list = self.generate_positions(self.bom_list)
        else:
            self.bom_list = pd.DataFrame({"Checked": []})
        
        self.trigger_event("bom_changed")

    def generate_positions(self, df):
        df['Parent'] = df['Parent'].fillna('')
        df = df.sort_values(by=['Parent', 'Balloon'])

        positions = {}
        position_count = {}

        def assign_position(child, parent_position):
            children = df[df['Parent'] == child].sort_values(by='Balloon')
            for idx, child_row in enumerate(children.itertuples(), start=1):
                child_position = f"{parent_position}.{idx}" if parent_position else f"{idx}"
                positions[(child_row.Child, child_row.Parent)] = child_position
                position_count[(child_row.Child, child_row.Parent)] = idx

                #print(f"Assigned position {child_position} to {child_row.Child} with parent {child_row.Parent}")
                assign_position(child_row.Child, child_position)

        top_level_items = df[df['Parent'] == ''].sort_values(by='Balloon')
        for idx, item in enumerate(top_level_items.itertuples(), start=1):
            top_position = f"{idx}"
            positions[(item.Child, item.Parent)] = top_position
            #print(f"Assigned top-level position {top_position} to {item.Child}")
            assign_position(item.Child, top_position)

        # Apply positions to the DataFrame
        df['Position'] = df.apply(lambda row: positions.get((row['Child'], row['Parent']), None), axis=1)

        # Check and assign positions for any remaining orphan nodes
        for row in df.itertuples():
            if row.Position is None:
                parent_position = positions.get((row.Parent, ''), '')
                if parent_position:
                    siblings = df[df['Parent'] == row.Parent]
                    child_position = f"{parent_position}.{len(siblings) + 1}"
                    positions[(row.Child, row.Parent)] = child_position
                    position_count[(row.Parent,)] = position_count.get((row.Parent,), 0) + 1
                    print(f"Reassigned position {child_position} to orphan {row.Child} with parent {row.Parent}")
                    df.at[row.Index, 'Position'] = child_position

        # Final check for any unassigned positions
        for row in df.itertuples():
            if row.Position is None:
                print(f"Warning: Unassigned position for {row.Child} with parent {row.Parent}")

        return df


