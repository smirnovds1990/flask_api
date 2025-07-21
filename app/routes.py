from flask import Blueprint, jsonify, Response

from app.services import ProductService

main_route = Blueprint("main", __name__)


@main_route.route("/info")
def info() -> Response:
    return jsonify({
        "total_products": ProductService().count_products(),
        "products": ProductService().get_products_info()
    })
