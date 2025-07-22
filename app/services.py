import time
from typing import Any

import requests
from flask import Flask
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.constants import MAIN_PRODUCTS_URL, NON_MAIN_PRODUCTS_URL
from app.db import db
from app.models import Category, Image, Parameter, Product, ProductMark
from app.schemas import (
    CategoryInSchema, ImageInSchema, ParameterInSchema, ProductInSchema,
    ProductMarkInSchema, ProductSchema
    )


def count_products() -> int:
    return db.session.scalar(db.select(db.func.count(Product.id)))


def get_products_info() -> list[dict[str, Any]]:
    products = db.session.execute(db.select(Product)).scalars().all()
    return [
        ProductSchema.from_orm(product).dict() for product in products
    ]


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


def save_categories(categories: list[CategoryInSchema]) -> None:
    for category in categories:
        category_id = category.Category_ID
        existing = db.session.get(Category, category_id)
        if not existing:
            new_category = Category(
                id=category_id,
                name=category.Category_Name,
                image=category.Category_Image,
                sort_order=category.sort_order,
            )
            db.session.add(new_category)
    db.session.commit()


def save_product_marks(product_marks: list[ProductMarkInSchema]) -> None:
    for mark in product_marks:
        mark_id = mark.Mark_ID
        existing = db.session.get(ProductMark, mark_id)
        if not existing:
            new_product_mark = ProductMark(
                id=mark_id, name=mark.Mark_Name
            )
            db.session.add(new_product_mark)
    db.session.commit()


def save_images(images: list[ImageInSchema]) -> None:
    for image in images:
        image_id = image.Image_ID
        existing = db.session.get(Image, image_id)
        if not existing:
            new_image = Image(
                id=image_id,
                image_url=image.Image_URL,
                main_image=image.MainImage,
                product_id=image.Product_ID,
                position=image.position if isinstance(image.position, int)
                else None,
                sort_order=image.sort_order,
                title=image.title,
            )
            db.session.add(new_image)
    db.session.commit()


def save_parameters(
    parameters: list[ParameterInSchema], product_id: int
) -> None:
    for parameter in parameters:
        parameter_id = parameter.Parameter_ID
        existing = db.session.get(Parameter, parameter_id)
        if not existing:
            new_parameter = Parameter(
                id=parameter_id,
                chosen=parameter.chosen,
                disabled=parameter.disabled,
                extra_field_color=parameter.extra_field_color,
                extra_field_image=parameter.extra_field_image,
                name=parameter.name,
                old_price=parameter.old_price,
                parameter_string=parameter.parameter_string,
                price=parameter.price,
                sort_order=parameter.sort_order,
                product_id=product_id,
            )
            db.session.add(new_parameter)
    db.session.commit()


def save_product(product: ProductInSchema) -> None:
    product_id = product.Product_ID
    existing = db.session.get(Product, product_id)
    if not existing:
        new_product = Product(
            id=product_id,
            on_main=product.OnMain,
            name=product.Product_Name,
        )
        db.session.add(new_product)
    db.session.commit()


def save_products_with_nested_objects(products: list[ProductInSchema]) -> None:
    for product in products:
        save_product(product)
        new_product = db.session.get(Product, product.Product_ID)
        save_categories(product.categories)
        save_images(product.images)
        save_parameters(product.parameters, product.Product_ID)
        new_product.categories = [
            db.session.get(Category, cat.Category_ID)
            for cat in product.categories
        ]
        new_product.images = [
            db.session.get(Image, img.Image_ID)
            for img in product.images
        ]
        new_product.parameters = [
            db.session.get(Parameter, param.Parameter_ID)
            for param in product.parameters
        ]
        db.session.add(new_product)
    db.session.commit()


def load_fetched_data_to_db(app: Flask) -> None:
    """Load all fetched data to DB. Work as a background task."""
    while True:
        with app.app_context():
            try:
                data = fetch_products_data()
                product_marks = [
                    ProductMarkInSchema(**mark) for mark
                    in data["product_marks"]
                ]
                products = [
                    ProductInSchema(**prod) for prod in data["products"]
                ]
                save_product_marks(product_marks)
                app.logger.info("Отметки на продуктах обновлены")
                save_products_with_nested_objects(products)
                app.logger.info(
                    "Продукты, категории, изображения, параметры обновлены."
                )
            except RequestException as e:
                app.logger.error(f"Ошибка запроса к API: {e}")
            except SQLAlchemyError as e:
                app.logger.error(f"Ошибка базы данных: {e}")
            except (ValueError, TypeError, KeyError) as e:
                app.logger.error(f"Ошибка обработки данных: {e}")
        time.sleep(app.config["FETCH_INTERVAL"])
