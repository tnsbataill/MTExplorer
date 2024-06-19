"""controller for bom browser window"""

import os.path
from tkinter import StringVar
from PIL import Image, ImageTk
from model.main import Model
from view.main import View

class BomBrowserController:
    """controller class for bom browser window"""

    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.load_images()
        self.frame = self.view.frames["bombrowser"]
        self.sv = StringVar()
        self._bind()
        self.boms_refresh()


    def _bind(self) -> None:
        self.sv.trace_add("write", self.filter_change)
        self.frame.filter_entry.config(textvariable=self.sv)
        self.frame.boms_list.bind("<Double-1>",self.bom_select)
        self.frame.boms_list.heading("M-Number",command=self.boms_sort("M-Number"))
        self.frame.boms_list.heading("Job Number",command=self.boms_sort("Job Number"))
        self.frame.boms_list.heading("Job Name",command=self.boms_sort("Job Name"))
        self.frame.bom_list.bind("<<TreeviewSelect>>", self.dwg_select)
        self.frame.filter_clear_btn.config(command=self.filter_clear)

    def load_images(self) -> None:
        icon_size = 20
        im = Image.open("images/Part.png").resize([icon_size, icon_size])
        self.part_image = ImageTk.PhotoImage(im)
        im = Image.open("images/Assembly.png").resize([icon_size, icon_size])
        self.assy_image = ImageTk.PhotoImage(im)
        im = Image.open("images/purch.png").resize([icon_size, icon_size])
        self.purch_image = ImageTk.PhotoImage(im)
        im = Image.open("images/Drawing.png").resize([icon_size, icon_size])
        self.dwg_image = ImageTk.PhotoImage(im)
        im = Image.open("images/Info.png").resize([icon_size, icon_size])
        self.info_image = ImageTk.PhotoImage(im)


    def filter_clear(self) -> None:
        """Empty the selection filter"""
        self.sv.set("")

    def filter_change(self, *args) -> None:
        """action for change of filter"""
        self.model.boms.boms_filter(self.frame.filter_entry.get())

    def bom_select(self, *args) -> None:
        """function call for bom selection change"""
        selection = self.frame.boms_list.selection()
        selection_text = self.frame.boms_list.item(selection)['text']
        self.model.bom.change(selection_text)

    def dwg_select(self, *args) -> None:
        cur_item = self.frame.bom_list.focus()
        if cur_item[0] == "M":
            cur_vals = self.frame.bom_list.item(cur_item)
            if cur_vals.get("values")[4] != "None":
                cur_filename: str = cur_vals.get("values")[4]
                cur_filetype = os.path.splitext(cur_filename)[1]
                self.load_file(cur_filename, cur_filetype)

    def load_file(self, cur_filename: str, cur_filetype: str) -> None:
        match cur_filetype:
            case '.PDF':
                pdf_doc = fitz.open(cur_filename)
                for page  in pdf_doc:
                    pix = page.get_pixmap(alpha=False)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    canvas_width = self.frame.dwg_preview.winfo_width()
                    canvas_height = self.frame.dwg_preview.winfo_height()
                    scale_factor = min(canvas_width / img.width, canvas_height / img.height)
                    img = img.resize((int(img.width * scale_factor), int(img.height * scale_factor)), Image.Resampling.LANCZOS)
                print("Loading preview image:", cur_filename)
                #self.frame.dwg_preview.delete("all")
                self.frame.dwg_preview.create_image(50,50, anchor='center', image=ImageTk.PhotoImage(img))

    def bom_refresh(self)-> None:
        """Deletes and reloads the BOM list"""
        if self.model.bom.bom_list is not None:
            for row in self.frame.bom_list.get_children():
                self.frame.bom_list.delete(row)
            for item in self.model.bom.bom_list.iloc:
                if not self.frame.bom_list.exists(item['Child']):
                    item_iid = item['Child']
                    item_parent = item['Parent']
                elif item['Path'] == '':    #case for top level assy
                    item_iid = item['Child']
                else:
                    item_iid = item['Child'] + str(item.name)
                    item_parent = item['Child']

                match item['listASP']:
                    case "A": item_image = self.assy_image
                    case "S": item_image = self.assy_image
                    case "P":
                        if item['Child'][0] == "M":
                            item_image = self.part_image
                        else:
                            item_image = self.purch_image
                    case "Z": item_image = self.info_image
                    case None: item_image = self.assy_image

                self.frame.bom_list.insert(item_parent, 'end', iid=item_iid, 
                                           text='', image=item_image, values=(
                                           item['Balloon'], item['Mnumber'], int(item['Qty']),
                                           item['Name'], item['FileName']))


    def boms_sort(self, sort_header) -> None:
        """sorts the BOMs treeview"""
        self.model.boms.boms_sort(sort_header)

    def boms_refresh(self) -> None:
        """Deletes and reloads the BOMs list"""
        if self.model.boms.bomslist is not None:
            for row in self.frame.boms_list.get_children():
                self.frame.boms_list.delete(row)
            for item in self.model.boms.bomslist.iloc:
                self.frame.boms_list.insert('', 'end', text=item[0],
                                            values=(item[0], item[4], item[1]))
