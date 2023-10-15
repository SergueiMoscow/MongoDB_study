import os
import sys

import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.schemas.user import CreateUser

# Добавляем путь к модулю tests в переменную PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_for_delete(faker):
    def _create_user(
        login: str | None = None,
        password: str | None = None,
        name: str | None = None,
        is_superuser: bool = False,
    ):
        if name is None:
            name = faker.unique.name()
        if password is None:
            password = faker.password()
        if login is None:
            login = faker.first_name()
        return CreateUser(
            login=login,
            password=password,
            name=name,
            is_superuser=is_superuser,
        )

    return _create_user
