from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, func, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db, products_categories, product_marks


class Category(db.Model):
    """Provides products categories."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str | None]
    name: Mapped[str] = mapped_column(String(150))
    sort_order: Mapped[int | None] = mapped_column(default=0)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary=products_categories,
        back_populates="categories",
    )


class ProductMark(db.Model):
    """Represents any special mark on a product."""

    __tablename__ = "product_marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    products: Mapped[list["Product"]] = relationship(
        secondary=product_marks, back_populates="marks"
    )


class Image(db.Model):
    """Represents images."""

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(1024))
    main_image: Mapped[bool] = mapped_column(Boolean, default=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    position: Mapped[int | None]
    sort_order: Mapped[int | None] = mapped_column(default=0)
    title: Mapped[str | None]

    product: Mapped["Product"] = relationship(
        "Product", back_populates="images"
    )


class Parameter(db.Model):
    """Represents parameters for products."""

    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(primary_key=True)
    chosen: Mapped[bool | None] = mapped_column(Boolean, default=False)
    disabled: Mapped[bool | None] = mapped_column(Boolean, default=False)
    extra_field_color: Mapped[str | None]
    extra_field_image: Mapped[str | None]
    name: Mapped[str | None]
    old_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    parameter_string: Mapped[str | None]
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    sort_order: Mapped[int | None] = mapped_column(default=0)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))

    product: Mapped["Product"] = relationship(
        "Product", back_populates="parameters"
    )


class Product(db.Model):
    """Represents products."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    on_main: Mapped[bool] = mapped_column(Boolean, default=True)
    name: Mapped[str] = mapped_column(String(255))

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=products_categories,
        back_populates="products",
    )
    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="product"
    )
    parameters: Mapped[list["Parameter"]] = relationship(
        "Parameter", back_populates="product"
    )
    marks: Mapped[list["ProductMark"]] = relationship(
        secondary=product_marks, back_populates="products"
    )
