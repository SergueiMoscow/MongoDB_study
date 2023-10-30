import time

import pymongo.collection
from pymongo import DESCENDING

from api.schemas.common import Pagination
from api.schemas.order import CreateOrder, Order, Sorting
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
    def get_custom_list(
            cls,
            pagination: Pagination,
            query: dict,
            sort_by: str | None = None,
            sorting: Sorting | None = None,
    ):
        skip_records = cls._get_skip_records(pagination.page, pagination.limit)

        if sort_by and sorting:
            cursor = (
                cls._collection.find(query)
                .sort(sort_by, cls._get_order_direction(sorting))
                .skip(skip_records)
                .limit(pagination.limit)
            )
        else:
            cursor = cls._collection.find(query).skip(skip_records).limit(pagination.limit)
        return cls._get_list_from_cursor(cursor)

    @classmethod
    def get_average_order_amount(cls, start_date: int = 0, end_date: int = int(time.time())):
        pipeline = [
            {"$match": {"created": {"$gte": start_date, "$lt": int(end_date)}}},
            {"$unwind": "$items"},
            {'$project': {'total': {'$multiply': ['$items.quantity', '$items.price']}}},
            {'$group': {'_id': '$orderId', 'total': {'$sum': '$total'}}},
            {'$group': {'_id': None, 'average': {'$avg': '$total'}}}
        ]

        average_list = list(cls._collection.aggregate(pipeline))
        average_value = average_list[0]["average"]
        return average_value

    @classmethod
    def get_popular_products_list(cls, start_date: int = 0, end_date: int = int(time.time())):
        pipeline = [
            {"$match": {"created": {"$gte": start_date, "$lt": int(end_date)}}},
            {"$unwind": "$items"},
            {
                "$group":
                {
                    "_id": "$items.product_id",
                    "name": {"$first": "$items.name"},
                    "total": {"$sum": "$items.quantity"}
                }
            },
            {"$sort": {"total": DESCENDING}}
        ]
        records = cls._collection.aggregate(pipeline)
        return list(records)
