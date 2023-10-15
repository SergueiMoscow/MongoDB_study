import re
from typing import List

import pytest

from api.schemas.product import CreateProduct, Product
from api.schemas.user import CreateUser, User
from db.client import mongo_client, mongo_db
from repositories.products import ProductRepository
from repositories.users import UserRepository

LEN_TEST_MULTIPLE_RECORDS = 10


@pytest.fixture
def db_for_test():
    yield mongo_db
    if 'test' in mongo_db.name:
        mongo_client.drop_database(mongo_db.name)
    db_list = mongo_client.list_database_names()
    pattern = re.compile(r'.*_test_.*')
    for db in db_list:
        if pattern.match(db):
            mongo_client.drop_database(db)


@pytest.fixture
@pytest.mark.usefixtures('db_for_test')
def created_multiple_products(faker) -> List[Product]:
    products = [
        CreateProduct(
            name=faker.unique.name(),
            category=faker.name(),
            price=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
        )
        for _ in range(LEN_TEST_MULTIPLE_RECORDS)
    ]
    result = []
    for product in products:
        new_object_id = ProductRepository.create(product.model_dump()).inserted_id
        result.append(Product(_id=new_object_id, **product.model_dump()))
    return result


@pytest.fixture
@pytest.mark.usefixtures('db_for_test')
def created_multiple_users(create_user) -> List[User]:
    users = [create_user() for _ in range(LEN_TEST_MULTIPLE_RECORDS)]
    result = []
    for user in users:
        new_object_id = UserRepository.create(user.model_dump()).inserted_id
        result.append(User(_id=new_object_id, **user.model_dump()))
    return result


@pytest.fixture
def product(faker):
    def _create_product(
        name: str | None = None,
        category: str | None = None,
        price: float | None = None,
    ):
        if name is None:
            name = faker.unique.name()
        if category is None:
            category = faker.name()
        if price is None:
            price = faker.pydecimal(left_digits=3, right_digits=2, positive=True)
        return CreateProduct(
            name=name,
            category=category,
            price=price,
        )

    return _create_product


@pytest.fixture
def create_user(faker):
    def _create_user(
        login: str | None = None,
        password: str | None = None,
        name: str | None = None,
        is_superuser: bool = False,
    ):
        if name is None:
            name = f'{faker.unique.first_name()}_{faker.unique.last_name()}'
        if password is None:
            password = faker.password()
        if login is None:
            login = f'{faker.first_name()}_{faker.unique.bothify("###")}'
        return CreateUser(
            login=login,
            password=password,
            name=name,
            is_superuser=is_superuser,
        )

    return _create_user


@pytest.fixture
def user(faker):
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
        return User(
            _id=faker.unique.bothify('619e8f45ee462d6d###bbd##'),
            login=login,
            password=password,
            name=name,
            is_superuser=is_superuser,
        )

    return _create_user
