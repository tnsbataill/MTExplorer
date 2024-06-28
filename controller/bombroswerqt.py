# bombrowser.py
import os.path
import string
from PySide6.QtCore import Qt, Slot, QCoreApplication, QRunnable, QThreadPool
import concurrent.futures
from sqlalchemy import false, true
", QVariant"
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QTreeWidgetItem
from model.main import Model
from view.main import View

class BomBrowserController:
    """controller class for bom browser window"""

    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.ui = self.view.root.ui
        self._ui_setup()
        self._bind()
        self.boms_refresh()
        self.thread_pool = QThreadPool()
        self.loading_state("show")

    def _ui_setup(self) -> None:
        self.ui.loading_bar.setMinimum(0)
        self.ui.loading_bar.setMaximum(0)
        self.loading_state("show")

    def _bind(self) -> None:
        self.ui.filterTextInput.textChanged.connect(self.filter_change)
        #self.ui.BOMtreeWidget.doubleClicked.connect(self.bom_select)
        self.ui.filterClearButton.clicked.connect(self.filter_clear)
        self.ui.projectComboBox.currentIndexChanged.connect(self.bom_select)
        self.ui.projectComboBox.currentIndexChanged.connect(self.loading_state("show"))
        self.ui.BOMtreeWidget.expanded.connect(self.node_clicked)
        self.ui.BOMtreeWidget.collapsed.connect(self.node_clicked)

    @Slot()
    def filter_clear(self) -> None:
        """Empty the selection filter"""
        self.ui.filterTextInput.setPlainText("")

    @Slot()
    def filter_change(self) -> None:
        """action for change of filter"""
        self.model.boms.boms_filter(self.ui.filterTextInput.toPlainText())

    @Slot(int)
    def bom_select(self, index: int) -> None:
        """function call for bom selection change"""
        selection_text = self.ui.projectComboBox.itemText(index)
        self.model.bom.change(selection_text[:11])
    
    @Slot(int)
    def node_clicked(self) -> None:
        self.ui.BOMtreeWidget.resizeColumnToContents(0)

    @Slot()
    def dwg_select(self) -> None:
        cur_item = self.ui.BOMtreeWidget.currentItem()
        if cur_item.text(0)[0] == "M":
            cur_vals = cur_item.text(4)
            if cur_vals != "None":
                cur_filename = cur_vals
                cur_filetype = os.path.splitext(cur_filename)[1]
                self.load_file(cur_filename, cur_filetype)

    @Slot()
    def openComboBox(self) -> None:
        self.ui.projectComboBox.showPopup()

    def load_file(self, cur_filename: str, cur_filetype: str) -> None:
        # TODO: add in pdf editor 
        pass

    def _item_exists_in_tree(self, child_id: str) -> bool:
        """Check if an item with the given child_id exists in the QTreeWidget."""
        root = self.ui.BOMtreeWidget.invisibleRootItem()
        return self._search_tree(root, child_id)
    
    def _search_tree(self, parent_item, child_id: str) -> bool:
        for i in range(parent_item.childCount()):
            child_item = parent_item.child(i)
            if child_item.text(0) == child_id:
                return True
            if self._search_tree(child_item, child_id):
                return True
        return False
    
    class RefreshTask(QRunnable):
        def __init__(self, controller):
            super().__init__()
            self.controller = controller

        def run(self):
            self.controller._refresh()

    def bom_refresh(self) -> None:
        """Deletes and reloads the BOM list"""
        self.loading_state("show")
        QCoreApplication.processEvents()  # Process events to update UI
        task = self.RefreshTask(self)
        self.thread_pool.start(task)

    def _find_item_by_iid(self, iid):
        root = self.ui.BOMtreeWidget.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            if item.text(0) == iid:  # Assuming the IID is in the first column
                return item
        return None

    def _get_item_image(self, listASP, child):
        image_path = None
        if listASP in ["A", "S"]:
            image_path = ":/icons/Assembly.png"
        elif listASP == "P":
            image_path = ":/icons/Part.png" if child[0] == "M" else ":/icons/purch.png"
        elif listASP == "Z":
            image_path = ":/icons/Info.png"
        else:
            image_path = ":/icons/Assembly.png"
        
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")

        # Resize the pixmap to the desired icon size (e.g., 16x16 pixels)
        icon_size = 32
        pixmap = pixmap.scaled(icon_size, icon_size, \
            Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

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
        self.ui.projectComboBox.clear()
        if self.model.boms.bomslist is not None:
            for item in self.model.boms.bomslist.iloc:
                # Create a display string for the combo box item with multiple columns
                display_text = f"{item.iloc[0]} | {item.iloc[4]} | {item.iloc[1]}"
                self.ui.projectComboBox.addItem(display_text)

    @Slot()
    def loading_state(self, state: str) -> None:
        if state == "show":
            self.ui.loading_bar.show()
            self.ui.loading_label.show()
        elif state == "hide":
            self.ui.loading_bar.hide()
            self.ui.loading_label.hide()
        else:
            print(f"Error: Incorrect argument for loading state: {state}")

    def _refresh(self):
        self.ui.BOMtreeWidget.setEnabled(False)
        self.ui.BOMtreeWidget.clear()

        if self.model.bom.bom_list is not None:
            tree_items = {}
            for item in self.model.bom.bom_list.iloc():
                #item_iid =  item['Child']
                item_iid = item['PurNo'] if item['Child'][0] == "Z" else item['Child']
                item_qty = str(int(item['Qty'])) if item['Qty'] > 0 else ""
                item_position = item['Position']
                item_image = self._get_item_image(item['listASP'], item['Child'])
                tree_item = QTreeWidgetItem([
                    item_iid, item['Balloon'], item_qty, 
                    item['Name']
                ])
                tree_item.setIcon(0, item_image)

                if item_position in tree_items:
                    pass
                else:
                    if '.' in item_position:
                        parent_position = '.'.join(item_position.split('.')[:-1])
                        parent_item = tree_items.get(parent_position, None)
                        if parent_item:
                            parent_item.addChild(tree_item)
                        else:
                            self.ui.BOMtreeWidget.addTopLevelItem(tree_item)
                    else:
                        self.ui.BOMtreeWidget.addTopLevelItem(tree_item)
                    tree_items[item_position] = tree_item

                if not self._item_exists_in_tree(item['Child']):
                    item_parent = item['Parent']
                elif item['Path'] == '':
                    item_iid = item['Child']

            for i in range(self.ui.BOMtreeWidget.columnCount()):
                self.ui.BOMtreeWidget.resizeColumnToContents(i)
            first_item = self.ui.BOMtreeWidget.topLevelItem(0)
            self.ui.BOMtreeWidget.expandItem(first_item)

        self.ui.BOMtreeWidget.setEnabled(True)
        QCoreApplication.processEvents()  # Process events to update UI
        self.loading_state("hide")