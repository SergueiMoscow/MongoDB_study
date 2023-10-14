import pymongo

from db.settings import db_settings

mongo_client = pymongo.MongoClient(db_settings.DATABASE_URI)
mongo_db = mongo_client[db_settings.DATABASE_NAME]
