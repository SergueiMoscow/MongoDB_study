from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

from api.schemas.common import PER_PAGE
from api.schemas.product import CreateProduct, Product
from db.client import mongo_db


class ProductRepository:
    collection = mongo_db.products

    @classmethod
    def get_all_products(cls, page: int = 1, limit: int = PER_PAGE) -> list[Product]:
        skip_records = (page - 1) * limit
        cursor = cls.collection.find().skip(skip_records).limit(limit)
        result = []
        for product in cursor:
            product['id'] = str(product['_id'])
            result.append(Product(**product))
        return result

    @classmethod
    def get_product(cls, product_id: str) -> Product:
        cursor = cls.collection.find_one({'_id': ObjectId(product_id)})
        cursor['id'] = str(cursor['_id'])
        return Product(**cursor)

    @classmethod
    def create_product(cls, product: CreateProduct) -> InsertOneResult:
        product_dict = product.model_dump()
        # product_dict['id'] = bson.Binary.from_uuid(product_dict['id'])
        result = cls.collection.insert_one(product_dict)
        return result

    @classmethod
    def update_product(cls, product_id: str, new_values: CreateProduct) -> bool:
        cursor = cls.collection.find_one({'_id': ObjectId(product_id)})
        if cursor:
            cursor.update(new_values.model_dump())
            # del cursor['_id']
            updated_product = cls.collection.update_one({'_id': ObjectId(product_id)}, {'$set': cursor})
            if updated_product:
                return True
        return False
