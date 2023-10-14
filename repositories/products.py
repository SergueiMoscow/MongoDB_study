from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

from api.schemas.common import PER_PAGE
from api.schemas.product import CreateProduct, Product
from db.client import mongo_db
from repositories.common import BaseRepository


class ProductRepository(BaseRepository):
    _collection = mongo_db.products
    _schema = Product
    _create_schema = CreateProduct
