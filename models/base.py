from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

class Base(DeclarativeBase):
  pass

engine = create_engine("sqlite:///budget.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def log_sqlite_path(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA database_list;")
    print("📦 SQLite is connected to:", cursor.fetchall())
    cursor.close()