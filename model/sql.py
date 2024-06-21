"""SQL interactions"""

from time import time
from tkinter import messagebox
from typing import Optional
from sqlalchemy import create_engine
import pandas as pd

def get_datatable(self, sqlstring: str) -> Optional[pd.DataFrame]:
    """retrieves the datatable based on request string"""
    database_url = "mssql+pyodbc://NAmtsql/Matix?trusted_connection=yes&driver=SQL+Server"
    database_url_fallback = "mssql+pyodbc://TESTUSER:testuser123@TN5715-L103/Matix?driver=SQL+Server"
    
    self.matixsqldb = None
    self.returnstring = None
    self.table = None

    try:
        start_time = time()
        # Create an SQLAlchemy engine
        engine = create_engine(database_url)
        # Use the engine in pandas.read_sql
        table = pd.read_sql(sqlstring, engine)
        comm_time = round(time() - start_time, 4)
        print(f"Database connection complete, communication time {comm_time}s")
    except Exception as error:
        messagebox.showerror(title="SQL Error", message=str(error))
        print("Connection failed", error)
        table = None

    return table