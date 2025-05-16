from typing import List, Optional
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    archived: Mapped[bool] = mapped_column(default=False)
    budget_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship(
        back_populates="tags"
    )
    
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="tag", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tag({self.name}>"
    
    def to_dict(self, include_transactions: bool=False):
        data = {
            "id": self.id,
            "category_id": self.category_id,
            "category": self.category.to_dict(False,False),
            "name": self.name,
            "archived": self.archived,
            "accumulated": self.accumulated(),
            "budget_amount": self.budget_amount
        }
        if include_transactions:
            data["transactions"] = [tx.to_dict(False,False) for tx in self.transactions]

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