import urllib

from sqlalchemy import create_engine, or_, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = dict(driverDB="{ODBC Driver 17 for SQL Server}",
          serverDB="localhost",
          portDB="1433",
          userDB="localhost")

conn_str = (f"Driver={db['driverDB']}"
            f";Server={db['serverDB']}"
            f";Port={db['portDB']}"
            f";UID={db['userDB']}"
            ";TrustServerCertificate=no")

quoted_conn_str = urllib.parse.quote_plus(conn_str)
engine = create_engine("mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()