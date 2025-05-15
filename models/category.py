from typing import List, Optional
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    archived: Mapped[bool] = mapped_column(default=False)
    budget_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)

    tags: Mapped[List["Tag"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category({self.name}>"
    
    def to_dict(self, include_tags: bool=True, include_transactions: bool=False):
        data = {
            "id": self.id,
            "name": self.name,
            "archived": self.archived,
            "accumulated": self.accumulated(),
            "budget_amount": self.budget_amount
        }
        if include_tags:
            data["tags"] = [tag.to_dict() for tag in self.tags]
        if include_transactions:
            data["transactions"] = [tx.to_dict(False, False) for tx in self.transactions]
        return data
    
    def accumulated(self):
        today = date.today()
        first = date(today.year, today.month, 1)
        last = date(today.year, today.month, self.get_last_day(today.year, today.month))
        transactions = self.transactions
        total = 0
        for transaction in transactions:
            if transaction.date >= first and transaction.date <= last:
                total += transaction.amount
        return total

    def get_last_day(self, year, month):
        isLeapYear = year % 400 == 0 or (year % 100 != 0 or year % 4 == 0)
        if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
            return 31
        elif month==4 or month==6 or month==9 or month==11:
            return 30
        elif month==2 and not isLeapYear:
            return 28
        else:
            return 29