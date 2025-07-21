import time
from typing import Any

import requests
from flask import Flask
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.constants import MAIN_PRODUCTS_URL, NON_MAIN_PRODUCTS_URL
from app.db import db
from app.models import Category, Product, ProductMark


def count_products() -> int:
    return db.session.scalar(db.select(db.func.count(Product.id)))


def get_products_info() -> list[Product]:
    products = db.session.execute(db.select(Product)).scalars().all()
    result = []
    for product in products:
        result.append({
            "name": product.name,
            "images": product.images,
            "prices": [str(p.price) for p in product.parameters],
            "categories": [c.name for c in product.categories],
        })
    return result


def merge_api_responses(
    main_response: dict[str, Any],
    non_main_response: dict[str, Any],
) -> dict[str, Any]:
    products = main_response["products"] + non_main_response["products"]
    return {
        "categories": main_response["categories"],
        "product_marks": main_response["product_marks"],
        "products": products,
    }


def fetch_products_data() -> dict[str, Any]:
    """Fetch data from source URLs and return total results."""
    main_page_response = requests.get(MAIN_PRODUCTS_URL).json()
    non_main_page_response = requests.get(NON_MAIN_PRODUCTS_URL).json()
    return merge_api_responses(main_page_response, non_main_page_response)


def save_categories(categories: dict[str, Any]) -> None:
    for category in categories:
        category_id = category["Category_ID"]
        existing = db.session.get(Category, category_id)
        if not existing:
            new_category = Category(
                id=category_id,
                name=category["Category_Name"],
                image=category["Category_Image"],
                sort_order=category["sort_order"],
            )
            db.session.add(new_category)
    db.session.commit()


def save_product_marks(product_marks: dict[str, Any]) -> None:
    for mark in product_marks:
        mark_id = mark["Mark_ID"]
        existing = db.session.get(ProductMark, mark_id)
        if not existing:
            new_product_mark = ProductMark(
                id=mark["Mark_ID"], name=mark["Mark_Name"]
            )
            db.session.add(new_product_mark)
    db.session.commit()


def load_fetched_data_to_db(app: Flask) -> None:
    """Load all fetched data to DB. Work as a background task."""
    while True:
        with app.app_context():
            try:
                data = fetch_products_data()
                save_categories(data["categories"])
                app.logger.info("Категории обновлены")
                save_product_marks(data["product_marks"])
                app.logger.info("Отметки на продуктах обновлены")
            except RequestException as e:
                app.logger.error(f"Ошибка запроса к API: {e}")
            except SQLAlchemyError as e:
                app.logger.error(f"Ошибка базы данных: {e}")
            except (ValueError, TypeError, KeyError) as e:
                app.logger.error(f"Ошибка обработки данных: {e}")
        time.sleep(app.config["FETCH_INTERVAL"])
