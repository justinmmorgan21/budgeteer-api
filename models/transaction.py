import pdfplumber
import re
from sqlalchemy import Column, String, Float, Integer
from .base import Base

class Transaction(Base):
  __tablename__ = "transactions"

  id = Column(Integer, primary_key=True)
  type = Column(String)
  date = Column(String)
  amount = Column(Float)
  payee = Column(String)


  def __repr__(self):
      return f"<Transaction({self.type}, {self.date}, {self.amount}, {self.payee}>"
  
  def to_dict(self):
      return {
          "id": self.id,
          "type": self.type,
          "date": self.date,
          "amount": self.amount,
          "payee": self.payee,
      }
  
  @staticmethod
  def parseLine(line, transactions):
    index = line.find(" ")
    date = line[0:index]
    remainder = line[index + 1:]
    index = remainder.find(" ")
    amount = remainder[0:index]
    tx_type = "DEPOSIT"
    if (amount[0] == "("):
        tx_type = "WITHDRAWAL"   
        amount = amount[1:-1]
    payee = remainder[remainder.find(" ") + 1:]
    return Transaction(type=tx_type, date=date, amount=float(amount.replace(",","")), payee=payee)

  @staticmethod
  def read_statement(pdf_path):
      transactions = []
      with pdfplumber.open(pdf_path) as pdf:
          for i in range(7):
              page = pdf.pages[i]
              cropped = page.crop((0, 0.1 * float(page.height), page.width, page.height))
              page_text = cropped.extract_text()
              lines = page_text.splitlines()
              for line in lines:
                  if re.search("^[0-9]+/[0-9]+/", line):
                      transactions.append(Transaction.parseLine(line, transactions))
      return transactions