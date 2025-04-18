from typing import List, Optional
from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date

class Category_Tag(Base):
  __tablename__ = "category_tags"

  id: Mapped[int] = mapped_column(primary_key=True)
  category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
  tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

  category: Mapped["Category"] = relationship(back_populates="category_tags")
  tag: Mapped["Tag"] = relationship(back_populates="category_tags")


  transactions: Mapped[List["Transaction"]] = relationship(
    back_populates="category_tag", cascade="all, delete-orphan"
  )

  def __repr__(self):
      return f"<Category_Tag({self.category_id}, {self.tag_id}>"
  
  def to_dict(self, include_relations=False, include_transactions=False):
      data = {
          "id": self.id,
          "category_id": self.category_id,
          "tag_id": self.tag_id,
      }
      if include_relations:
         data["category"] = self.category.to_dict() if self.category else None
         data["tag"] = self.tag.to_dict() if self.tag else None
      if include_transactions:
         data["transactions"] = [t.to_dict(include_category_tag=False) for t in self.transactions]
      
      return data