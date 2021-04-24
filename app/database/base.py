import urllib

from sqlalchemy import create_engine, or_, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = dict(driverDB="{ODBC Driver 17 for SQL Server}",
          serverDB="DESKTOP-KSACHTT\SQLEXPRESS",
          portDB="1433",
          userDB="adminV",
          database="CHAL",
          passwordDB="CHAOSSHIT2")

conn_str = (f"Driver={db['driverDB']}"
            f";Server={db['serverDB']}"
            f";Port={db['portDB']}"
            f";Database={db['database']}"
            f";UID={db['userDB']}"
            f";PWD={db['passwordDB']}"
            ";TrustServerCertificate=no")

quoted_conn_str = urllib.parse.quote_plus(conn_str)
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted_conn_str))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()