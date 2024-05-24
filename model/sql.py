"""SQL interactions"""

from time import time
from tkinter import messagebox
from pyodbc import connect, Error
import pandas

def get_datatable(self, sqlstring: str) -> pandas.DataFrame:
    """retrieves the datatable based on request string"""
    self.connectionString = "Driver={SQL Server};Server=NAmtsql;Database=Matix;Trusted_Connection=True"
    self.connectionStringFallback = "Driver={SQL Server};Server=TN5715-L103;Uid=TESTUSER;Pwd=testuser123;"
    self.connectionStringFallbacker = "Driver={SQL Server};Provider=SQLOLEDB.1;Password=testuser123;User ID=TESTUSER;Initial Catalog=Matix;Data Source=TN5715-L103"
    self.matixsqldb = None
    self.returnstring = None
    self.table = None

    try:
        start_time = time()
        matixsqldb = connect(self.connectionString, timeout=3, readonly=True,)
        table = pandas.read_sql(sqlstring, matixsqldb)
        if matixsqldb is not None:
            matixsqldb.close()
            comm_time = round(time() - start_time, 4)
            print("Database connection complete, communication time", comm_time, "s")
    except Error as error:
        messagebox.showerror(title="Sql Error", message=error)
        print("Connection failed", error)
        table = None

    return table
