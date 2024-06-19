# bombrowser.py
import os.path
from PySide6.QtCore import Qt, Slot
", QVariant"
from PySide6.QtGui import QImage, QPixmap, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QTreeWidgetItem, QTreeWidget, QLineEdit, QPushButton
from model.main import Model
from view.main import View
import images.qresources_rc

class BomBrowserController:
    """controller class for bom browser window"""

    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.ui = self.view.root.ui
        self._bind()
        self.boms_refresh()

    def _bind(self) -> None:
        self.ui.filterTextInput.textChanged.connect(self.filter_change)
        self.ui.BOMtreeWidget.doubleClicked.connect(self.bom_select)
        self.ui.filterClearButton.clicked.connect(self.filter_clear)

        # header = self.frame.boms_list.headerItem()
        # head = self.ui.projectComboBox.
        # header.setText(0, "M-Number")
        # header.setText(1, "Job Number")
        # header.setText(2, "Job Name")

        # for col in range(header.columnCount()):
        #     header.setData(col, Qt.UserRole, QVariant(header.text(col)))
        #     header.setText(col, header.text(col))

        # self.frame.boms_list.header().sectionClicked.connect(self.boms_sort)

    @Slot()
    def filter_clear(self) -> None:
        """Empty the selection filter"""
        self.ui.filterTextInput.setPlainText("")

    @Slot()
    def filter_change(self) -> None:
        """action for change of filter"""
        self.model.boms.boms_filter(self.ui.filterTextInput.toPlainText())

    @Slot(QTreeWidgetItem, int)
    def bom_select(self, item: QTreeWidgetItem, column: int) -> None:
        """function call for bom selection change"""
        selection_text = item.text(0)
        self.model.bom.change(selection_text)

    @Slot()
    def dwg_select(self) -> None:
        cur_item = self.ui.BOMtreeWidget.currentItem()
        if cur_item.text(0)[0] == "M":
            cur_vals = cur_item.text(4)
            if cur_vals != "None":
                cur_filename = cur_vals
                cur_filetype = os.path.splitext(cur_filename)[1]
                self.load_file(cur_filename, cur_filetype)

    def load_file(self, cur_filename: str, cur_filetype: str) -> None:
        # TODO: add in pdf editor 
        pass

    def bom_refresh(self) -> None:
        """Deletes and reloads the BOM list"""
        self.ui.BOMtreeWidget.clear()
        if self.model.bom.bom_list is not None:
            for item in self.model.bom.bom_list.iloc:
                item_iid = item['Child']
                item_parent = item['Parent'] if item['Path'] != '' else ''
                item_image = self._get_item_image(item['listASP'], item['Child'])

                tree_item = QTreeWidgetItem([item['Balloon'], item['Mnumber'], str(int(item['Qty'])), item['Name'], item['FileName']])
                tree_item.setIcon(0, item_image)
                self.ui.BOMtreeWidget.addTopLevelItem(tree_item) if item_parent == '' else self._add_child_item(item_parent, tree_item)

    def _get_item_image(self, listASP, child):
        if listASP in ["A", "S"]:
            return QPixmap(":/images/icon.png")
        elif listASP == "P":
            return QPixmap(":/icons/Part.png") if child[0] == "M" else QPixmap(":/icons/purch.png")
        elif listASP == "Z":
            return QPixmap(":/icons/Info.png")
        else:
            return QPixmap(":/icons/Assembly.png")

    def _add_child_item(self, parent_id, child_item):
        for i in range(self.ui.BOMtreeWidget.topLevelItemCount()):
            parent_item = self.ui.BOMtreeWidget.topLevelItem(i)
            if parent_item.text(0) == parent_id:
                parent_item.addChild(child_item)
                break

    def boms_sort(self, index: int) -> None:
        """sorts the BOMs treeview"""
        header_text = self.ui.BOMtreeWidget.headerItem().text(index)
        self.model.boms.boms_sort(header_text)

    def boms_refresh(self) -> None:
        """Deletes and reloads the BOMs list"""
        self.ui.BOMtreeWidget.clear()
        if self.model.boms.bomslist is not None:
            for item in self.model.boms.bomslist.iloc:
                tree_item = QTreeWidgetItem([item[0], item[4], item[1]])
                self.ui.BOMtreeWidget.addTopLevelItem(tree_item)
