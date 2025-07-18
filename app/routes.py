import requests
from flask import Blueprint


from app.constants import MAIN_PRODUCTS_URL


main_route = Blueprint("main", __name__)


@main_route.route("/")
def get_products_info():
    response = requests.get(MAIN_PRODUCTS_URL)
    return response.json()["products"]
