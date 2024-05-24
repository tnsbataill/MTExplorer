from tkinter import Frame, Label, Entry, Button, Scrollbar, Canvas
from tkinter.ttk import Treeview

class BomBrowserView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        boms_cols = ("M-Number", "Job Number", "Job Name")
        bom_cols = ("Unit Number", "M-Number", "Quantity", "Name", "Checked", "Filename")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.search_frame = Frame(self)
        self.search_frame.grid(row=0, column=0)
        self.filter_label = Label(self.search_frame, text="Filter")
        self.filter_label.pack(side="left")
        self.filter_entry = Entry(self.search_frame)
        self.filter_entry.pack(side="left")
        self.filter_clear_btn = Button(self.search_frame, text="Clear Filter")
        self.filter_clear_btn.pack(side="left")

        self.boms_list_frame = Frame(self, padx=5, pady=5)
        self.boms_list_frame.grid(row=1, column=0, sticky="snew")
        self.boms_list = Treeview(self.boms_list_frame, columns=boms_cols,
                                  show="headings", selectmode="browse")
        self.boms_list.heading("M-Number", text="M-Number")
        self.boms_list.column("M-Number", stretch="No", width=90, anchor="center")
        self.boms_list.heading("Job Number", text="Job Number")
        self.boms_list.column("Job Number", stretch='No', width=90)
        self.boms_list.heading("Job Name", text="Job Name")
        self.boms_list.column("Job Name", stretch='no', width=300)
        self.boms_list.pack(side="left", fill="y")
        self.boms_list_scrl = Scrollbar(self.boms_list_frame, orient="vertical",
                                        command=self.boms_list.yview)
        self.boms_list_scrl.pack(side="left", fill="y")

        self.bom_list = Treeview(self, columns=bom_cols)
        self.bom_list.heading("#0", anchor="w")
        self.bom_list.column("#0", width=100, minwidth=25, stretch="No")
        self.bom_list.heading("Unit Number", text="Unit #")
        self.bom_list.column("Unit Number", stretch="No", width=60, anchor="center")
        self.bom_list.heading("M-Number", text="M-Number")
        self.bom_list.column("M-Number", stretch="No", width=90, anchor="center")
        self.bom_list.heading("Quantity", text="Quantity")
        self.bom_list.column("Quantity", stretch="No", width=60, anchor="center")
        self.bom_list.heading("Name", text="Name")
        self.bom_list.column("Name", stretch="Yes", anchor="center")
        self.bom_list.heading("Checked",text="✔")
        self.bom_list.column("Checked", stretch="No", width=25, anchor="center")
        self.bom_list.heading("Filename")
        self.bom_list.column("Filename", stretch="No", width=0)
        self.bom_list.grid(row=1, column=1, padx=5, pady=5, sticky="snew")

        self.dwg_preview = Canvas(self, bg="light grey")
        self.dwg_preview.grid(row=1, column=2, padx=5, pady=5, sticky="snew")
