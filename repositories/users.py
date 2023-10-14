from api.schemas.user import CreateUser, User
from db.client import mongo_db
from repositories.common import BaseRepository


class UserRepository(BaseRepository):
    _collection = mongo_db.users
    _schema = User
    _create_schema = CreateUser
