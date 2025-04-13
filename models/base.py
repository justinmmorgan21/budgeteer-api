from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

class Base(DeclarativeBase):
  pass

engine = create_engine("sqlite:///budget.db", echo=True)
SessionLocal = sessionmaker(bind=engine)