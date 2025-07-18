from datetime import datetime

from sqlalchemy import Boolean, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import db


class Category(db.Model):
    """Provides products categories."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str | None]
    name: Mapped[str] = mapped_column(String(150))
    sort_order: Mapped[int] = mapped_column(default=0)


class ProductMark(db.Model):
    """Represents any special mark on a product."""

    __tablename__ = "product_marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


# class Product(db.Model):
#     """Represents products."""

#     __tablename__ = "products"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )
#     on_main: Mapped[bool] = mapped_column(Boolean, default=True)
#     name: Mapped[str] = mapped_column(String(255))
