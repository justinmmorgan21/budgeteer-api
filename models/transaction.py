import pdfplumber
import re
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Numeric, DateTime, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import datetime, date
from decimal import Decimal
from .category import Category
from .tag import Tag
from sqlalchemy.orm import joinedload

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(10))
    date: Mapped[date]
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    payee: Mapped[str]
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tags.id"))
    
    category: Mapped[Optional["Category"]] = relationship(back_populates="transactions")
    tag: Mapped[Optional["Tag"]] = relationship(back_populates="transactions")

    def __repr__(self):
        return f"<Transaction({self.type}, {self.date}, {self.amount}, {self.payee})>"
    
    def to_dict(self, include_category: bool=True, include_tag: bool=True):
        return {
            "id": self.id,
            "type": self.type,
            "date": self.date,
            "amount": self.amount,
            "payee": self.payee,
            "category_id": self.category_id,
            "tag_id": self.tag_id,
            "category": self.category.to_dict(include_transactions=False) if include_category and self.category else None,
            "tag": self.tag.to_dict(include_transactions=False) if include_tag and self.tag else None
        }
  
    @staticmethod
    def filterQuery(session, request):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        search_term = request.args.get('search')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        uncategorized = request.args.get('uncategorized')

        query = session.query(Transaction).options(
            joinedload(Transaction.category).joinedload(Category.tags),
            joinedload(Transaction.tag)
        )
        if start_date and end_date:
            start_date_split = start_date.split('-')
            start_datetime = datetime(int(start_date_split[0]), int(start_date_split[1]), int(start_date_split[2]))
            end_date_split = end_date.split('-')
            end_datetime = datetime(int(end_date_split[0]), int(end_date_split[1]), int(end_date_split[2]))
            query = query.filter(
                Transaction.date.between(start_datetime, end_datetime)
            )
        if search_term:
            query = query.filter(
                or_(
                    Transaction.type.ilike(f"%{search_term}%"),
                    Transaction.payee.ilike(f"%{search_term}%")
                )
            )
        if uncategorized == "true":
            query = query.filter(
                or_(
                    Transaction.category_id == None,
                    Transaction.tag_id == None
                )
            )
        query = query.order_by(Transaction.date.desc())
        total_count = query.count()
        transactions = query.offset((page - 1) * per_page).limit(per_page).all()
        return {
            'transactions': [t.to_dict() for t in transactions],
            'total_pages': (total_count + per_page - 1) // per_page,
            'current_page': page
        }
  
    @staticmethod
    def parseLine(line, session):
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
        if payee.startswith("POSWithdrawal"):
            payee = payee[13:]
        if payee.startswith("ExternalWithdrawal"):
            payee = payee[18:]
        existing = session.query(Transaction).filter_by(payee=payee).order_by(Transaction.date.desc()).first()
        if not existing and payee.startswith("TransferDeposit ZelleFrom"):
            category = session.query(Category).filter_by(name='Income').first()
            tag = session.query(Tag).filter_by(name='hair').first()
            return Transaction(
                type=tx_type, date=date_obj, amount=amount, payee=payee,
                category_id=category.id if category else None,
                tag_id=tag.id if tag else None)
        return Transaction(
            type=tx_type, date=date_obj, amount=amount, payee=payee,
            category_id=existing.category_id if existing else None,
            tag_id=existing.tag_id if existing else None)

    @staticmethod
    def read_statement(pdf_path, session):
        transactions = []
        with pdfplumber.open(pdf_path) as pdf:
            for i in range(7):
                page = pdf.pages[i]
                cropped = page.crop((0, 0.1 * float(page.height), page.width, page.height))
                page_text = cropped.extract_text()
                lines = page_text.splitlines()
                for line in lines:
                    if re.search("^[0-9]+/[0-9]+/", line):
                        transactions.append(Transaction.parseLine(line, session))
        return transactions