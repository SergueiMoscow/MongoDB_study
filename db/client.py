import pymongo

from db.settings import db_settings

mongo_client: pymongo.MongoClient = pymongo.MongoClient(db_settings.DATABASE_URI)
mongo_db: pymongo.database.Database = mongo_client[db_settings.DATABASE_NAME]
