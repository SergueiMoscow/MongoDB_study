from api.schemas.order import Order, CreateOrder
from db.client import mongo_db
from repositories.common import BaseRepository


class OrderRepository(BaseRepository):
    _collection = mongo_db.orders
    _schema = Order
    _create_schema = CreateOrder
