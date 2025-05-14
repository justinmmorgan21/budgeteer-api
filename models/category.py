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
        transactions = self.transactions
        total = 0
        for transaction in transactions:
            total += transaction.amount
        return total
