from pymongo.results import InsertOneResult

from api.schemas.common import PER_PAGE
from api.schemas.product import CreateProduct, ProductResponse
from db.client import mongo_db


class ProductRepository:
    collection = mongo_db.products

    @classmethod
    def get_all_products(cls, page: int = 1, limit: int = PER_PAGE) -> list[ProductResponse]:
        skip_records = (page - 1) * limit
        cursor = cls.collection.find().skip(skip_records).limit(limit)
        result = []
        for product in cursor:
            # if product.get('id'):
            product['id'] = str(product['_id'])
            result.append(ProductResponse(**product))
        return result

    @classmethod
    def get_product(cls, product_id: str) -> ProductResponse:
        cursor = cls.collection.find_one({'_id': product_id})
        return ProductResponse(**cursor)

    @classmethod
    def create_product(cls, product: CreateProduct) -> InsertOneResult:
        product_dict = product.model_dump()
        # product_dict['id'] = bson.Binary.from_uuid(product_dict['id'])
        result = cls.collection.insert_one(product_dict)
        return result
