import pyodbc
import tkinter as tk
from tkinter import ttk

connectionString = "Driver={SQL Server};Server=NAmtsql;Database=Matix;Trusted_Connection=True"
jobListString = """SELECT [MATIX_E_BOM_LIST].HINBAN, [MATIX_E_BOM_LIST].HINMEI, [MATIX_E_BOM_LIST].YOBI_KATASHIKI, [MATIX_E_BOM_LIST].MATSUBI, [MATIX_E-JOB_NO].DESIGN_NO FROM [MATIX_E_BOM_LIST] LEFT OUTER JOIN [MATIX_E-JOB_NO] ON [MATIX_E_BOM_LIST].HINBAN like [MATIX_E-JOB_NO].HINBAN WHERE [MATIX_E_BOM_LIST].ASP_KBN = 'A' ORDER BY CASE WHEN DESIGN_NO IS NULL THEN 1 ELSE 0 END, DESIGN_NO;"""
bomListString = """SELECT [MATIX_E_BOM_LIST].HINBAN, [MATIX_E_BOM_LIST].HINMEI, [MATIX_E_BOM_LIST].YOBI_KATASHIKI, [MATIX_E_BOM_LIST].MATSUBI FROM [MATIX_E_BOM_LIST] WHERE [MATIX_E_BOM_LIST].ASP_KBN <> 'A' and [MATIX_E_BOM_LIST].HINBAN NOT LIKE '@%' ORDER BY HINBAN;"""

try:
    matixsqldb = pyodbc.connect(connectionString)
    cursor = matixsqldb.cursor()
    cursor.execute(jobListString)
    jobList = cursor.fetchall()
    cursor.execute(bomListString)
    bomList = cursor.fetchall()


except pyodbc.Error as error:
        print("Connection failed", error)
finally:
     if matixsqldb:
          matixsqldb.close()
          print("Connection Closed")




class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.listbox = tk.Listbox(self).grid(column=0, row=0)
        self.treeview = ttk.Treeview(self).grid(column=1, row=0)

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root, padding=10)
    root.mainloop()

    #################################

from tkinter import *

def Scankey(event):
	
	val = event.widget.get()
	print(val)
	
	if val == '':
		data = list
	else:
		data = []
		for item in list:
			if val.lower() in item.lower():
				data.append(item)				
	Update(data)
      
def Update(data):
	listbox.delete(0, 'end')
	
	for item in data:
		listbox.insert('end', item)

list = ('Salt','Sugar','Oil',
	'Toothpaste','Rice',
	'Pens','Fevicol','Notebooks' )

ws = Tk()
ws.title("Python Guides")
ws.geometry("500x300")


entry = Entry(ws)
entry.pack()
entry.bind('<KeyRelease>', Scankey)


listbox = Listbox(ws)
listbox.pack()
Update(list)

ws.mainloop()