from flask import Blueprint, jsonify, Response

from app.services import count_products, get_products_info

main_route = Blueprint("main", __name__)


@main_route.route("/info")
def info() -> Response:
    return jsonify({
        "total_products": count_products(),
        "products": get_products_info()
    })
