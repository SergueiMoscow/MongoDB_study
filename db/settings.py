import sys
import uuid
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class SettingsDataBase(BaseSettings):
    DATABASE_URI: str
    DATABASE_NAME: str

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / '.env', env_file_encoding='utf-8', extra='allow'
    )


db_settings = SettingsDataBase()

if 'pytest' in sys.modules:
    db_settings.DATABASE_NAME += '_test_' + str(uuid.uuid4()).replace('-', '_')


print(db_settings.DATABASE_URI)
print(db_settings.DATABASE_NAME)
