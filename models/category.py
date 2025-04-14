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

  category_tags: Mapped[List["Category_Tag"]] = relationship(
    back_populates="category", cascade="all, delete-orphan"
  )

  def __repr__(self):
    return f"<Category({self.name}>"
  
  def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "archived": self.archived,
        "category_tags": [ct.to_dict() for ct in self.category_tags]
    }