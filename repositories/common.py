from abc import ABC

from pymongo.results import InsertOneResult
from bson.objectid import ObjectId

from api.schemas.common import PER_PAGE
from api.schemas.user import User, CreateUser
from db.client import mongo_db


class BaseRepository(ABC):
    _collection = mongo_db.users
    _schema = User
    _create_schema = CreateUser

    @classmethod
    def get_all(cls, page: int = 1, limit: int = PER_PAGE) -> list[_schema]:
        skip_records = (page - 1) * limit
        cursor = cls._collection.find().skip(skip_records).limit(limit)
        result = []
        for record in cursor:
            record['id'] = str(record['_id'])
            result.append(cls._schema(**record))
        return result

    @classmethod
    def get_by_id(cls, record_id: str) -> _schema:
        cursor = cls._collection.find_one({'_id': ObjectId(record_id)})
        cursor['id'] = str(cursor['_id'])
        data = dict(cursor)
        return cls._schema.model_construct(**data)

    @classmethod
    def create(cls, record: dict) -> InsertOneResult:
        result = cls._collection.insert_one(record)
        return result

    @classmethod
    def update(cls, record_id: str, new_values: _create_schema) -> bool:
        cursor = cls._collection.find_one({'_id': ObjectId(record_id)})
        if cursor:
            cursor.update(new_values.model_dump())
            # del cursor['_id']
            updated_record = cls._collection.update_one({'_id': ObjectId(record_id)}, {'$set': cursor})
            if updated_record:
                return True
        return False
