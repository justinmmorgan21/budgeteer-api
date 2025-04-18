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

  category_tags: Mapped[List["Category_Tag"]] = relationship(
    back_populates="tag", cascade="all, delete-orphan"
  )

  def __repr__(self):
    return f"<Tag({self.name}>"
  
  def to_dict(self, include_transactions: bool=False):
    data = {
        "id": self.id,
        "name": self.name,
        "archived": self.archived,
    }
    if include_transactions:
      transactions = []
      for ct in self.category_tags:
        transactions.extend(ct.transactions)
      data["transactions"] = [tx.to_dict() for tx in transactions]

    return data