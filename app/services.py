from app.db import db
from app.models import Product


class ProductService:
    """Provides DB operations for Product model."""

    def count_products(self) -> int:
        return db.session.scalar(db.select(db.func.count(Product.id)))

    def get_products_info(self) -> list[Product]:
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
