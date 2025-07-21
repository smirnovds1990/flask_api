import time
from typing import Any

import requests
from flask import current_app
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.constants import MAIN_PRODUCTS_URL, NON_MAIN_PRODUCTS_URL
from app.db import db
from app.models import Product


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


def fetch_products_data() -> dict[str, Any]:
    """Fetch data from source URLs and return total results."""
    main_page_response = requests.get(MAIN_PRODUCTS_URL).json()
    non_main_page_response = requests.get(NON_MAIN_PRODUCTS_URL).json()
    return main_page_response + non_main_page_response


def parse_products_data(data: dict[str, Any]) -> dict[str, Any]:
    categories = data["categories"]
    product_marks = data["product_marks"]
    products = data["products"]
    return {
        "categories": categories,
        "product_marks": product_marks,
        "products": products,
    }


def save_products_data(objects: dict[str, Any]) -> None:
    pass


def load_fetched_data_to_db() -> None:
    """Load all fetched data to DB. Work as a background task."""
    while True:
        with current_app.app_context():
            try:
                data = fetch_products_data()
                objects_to_save = parse_products_data(data)
                save_products_data(objects_to_save)
                current_app.logger.info("Данные обновлены")
            except RequestException as e:
                current_app.logger.error(f"Ошибка запроса к API: {e}")
            except SQLAlchemyError as e:
                current_app.logger.error(f"Ошибка базы данных: {e}")
            except (ValueError, TypeError, KeyError) as e:
                current_app.logger.error(f"Ошибка обработки данных: {e}")
        time.sleep(current_app.config["FETCH_INTERVAL"])
