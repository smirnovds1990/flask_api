from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


products_categories = Table(
    "products_categories",
    Base.metadata,
    Column(
        "category_id", Integer, ForeignKey("categories.id"), primary_key=True
    ),
    Column(
        "product_id", Integer, ForeignKey("products.id"), primary_key=True
    ),
)
product_marks = Table(
    "product_marks_relations",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("mark_id", ForeignKey("product_marks.id"), primary_key=True),
)

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
