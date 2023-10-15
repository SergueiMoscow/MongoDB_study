from abc import ABC

from bson.objectid import ObjectId
from pymongo.results import InsertOneResult

from api.schemas.common import PER_PAGE
from api.schemas.user import CreateUser, User
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
    def get_by_id(cls, record_id: str) -> _schema | None:
        cursor = cls._collection.find_one({'_id': ObjectId(record_id)})
        if cursor is None:
            return None
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
            updated_record = cls._collection.update_one(
                {'_id': ObjectId(record_id)}, {'$set': cursor}
            )
            if updated_record:
                return True
        return False

    @classmethod
    def delete(cls, record_id: str) -> int:
        cursor = cls._collection.find_one({'_id': ObjectId(record_id)})
        if cursor:
            deleted = cls._collection.delete_one({'_id': ObjectId(record_id)})
            return deleted.deleted_count
        return 0

    @classmethod
    def get_by_field(cls, field_name: str, field_value: str) -> _schema | None:
        cursor = cls._collection.find_one({field_name: field_value})
        if cursor is None:
            return None
        cursor['id'] = str(cursor['_id'])
        data = dict(cursor)
        return cls._schema.model_construct(**data)
