import pdfplumber
import re

class Transaction:
  def __init__(self, type, date, amount, payee):
      self.type = type
      self.date = date
      self.amount = amount
      self.payee = payee

  def __str__(self):
      return self.type.upper() + " - " + self.date + ",  $" + self.amount + ",  payee: " + self.payee
  
  @staticmethod
  def parseLine(line, transactions):
    index = line.find(" ")
    date = line[0 : index]
    remainder = line[index + 1 :]
    index = remainder.find(" ")
    amount = remainder[0 : index]
    type = "**DEPOSIT**"
    if (amount[0] == "("):
        type = "**WITHDRAWAL**"   
        amount = amount[1: len(amount) - 1]
    payee = remainder[remainder.find(" ") + 1 : ]
    transactions.append(Transaction(type, date, amount, payee))

  @staticmethod
  def read_statement():
      transactions = []
      with pdfplumber.open("./src/models/BECU-Statement-21-Mar-2025.PDF") as pdf:
          for i in range(7):
              page = pdf.pages[i]
              cropped = page.crop((0, 0.1 * float(page.height), page.width, page.height))
              page_text = cropped.extract_text()
              lines = page_text.splitlines()
              for line in lines:
                  if re.search("^[0-9]+/[0-9]+/", line):
                      Transaction.parseLine(line, transactions)
      return transactions