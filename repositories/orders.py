import pymongo.collection

from api.schemas.common import Pagination
from api.schemas.order import CreateOrder, Order, OrderRequest, Sorting
from db.client import mongo_db
from repositories.common import BaseRepository


class OrderRepository(BaseRepository):
    _collection: pymongo.collection.Collection = mongo_db.orders
    _schema = Order
    _create_schema = CreateOrder

    @staticmethod
    def _get_order_direction(direction: Sorting) -> int:
        if direction and direction.value == 'desc':
            return pymongo.DESCENDING
        else:
            return pymongo.ASCENDING

    @classmethod
    def get_custom(
            cls,
            pagination: Pagination,
            query: dict,
            sort_by: str | None = None,
            sorting: Sorting | None = None
    ):
        skip_records = cls._get_skip_records(pagination.page, pagination.limit)

        if sort_by and sorting:
            cursor = (
                cls
                ._collection
                .find(query)
                .sort(sort_by, cls._get_order_direction(sorting))
                .skip(skip_records)
                .limit(pagination.limit)
            )
        else:
            cursor = cls._collection.find(query).skip(skip_records).limit(pagination.limit)
        return cls._get_list_from_cursor(cursor)
