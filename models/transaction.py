import pdfplumber
import re
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date
from decimal import Decimal

class Transaction(Base):
  __tablename__ = "transactions"

  id: Mapped[int] = mapped_column(primary_key=True)
  type: Mapped[str] = mapped_column(String(10))
  date: Mapped[date]
  amount: Mapped[float] = mapped_column(Numeric(10, 2))
  payee: Mapped[str]
  category_tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category_tags.id"))

  category_tag: Mapped["Category_Tag"] = relationship(back_populates="transactions")

  def __repr__(self):
      return f"<Transaction({self.type}, {self.date}, {self.amount}, {self.payee})>"
  
  def to_dict(self, include_category_tag: bool=True):
      return {
          "id": self.id,
          "type": self.type,
          "date": self.date,
          "amount": self.amount,
          "payee": self.payee,
          "category_tag_id": self.category_tag_id,
          "category_tag": self.category_tag.to_dict(include_relations=True, include_transactions=False) if include_category_tag and self.category_tag else None
      }
  
  @staticmethod
  def parseLine(line, transactions):
    index = line.find(" ")
    date_str = line[0:index]
    year = "20" + date_str[-2:]
    month = date_str[0:2]
    day = date_str[3:5]
    date_obj = date(int(year), int(month), int(day))
    remainder = line[index + 1:]
    index = remainder.find(" ")
    amount = remainder[0:index]
    tx_type = "DEPOSIT"
    if (amount[0] == "("):
        tx_type = "WITHDRAWAL"   
        amount = amount[1:-1]
    amount = Decimal(amount.replace(",",""))
    payee = remainder[remainder.find(" ") + 1:]
    return Transaction(type=tx_type, date=date_obj, amount=amount, payee=payee)

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