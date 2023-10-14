from typing import List
from fastapi.testclient import TestClient
from api.app import app
import pytest

from api.schemas.product import CreateProduct, Product
from db.client import mongo_client, mongo_db
from repositories.products import ProductRepository

LEN_TEST_PRODUCTS = 10


@pytest.fixture
def db_for_test():
    yield mongo_db
    if 'test' in mongo_db.name:
        mongo_client.drop_database(mongo_db.name)


@pytest.fixture
@pytest.mark.usefixtures('db_for_test')
def created_multiple_products(faker) -> List[Product]:
    products = [
        CreateProduct(
            name=faker.unique.name(),
            category=faker.name(),
            price=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
        )
        for _ in range(LEN_TEST_PRODUCTS)
    ]
    result = []
    for product in products:
        new_object_id = ProductRepository.create_product(product).inserted_id
        result.append(Product(_id=new_object_id, **product.model_dump()))
    return result


@pytest.fixture
def client():
    return TestClient(app)


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
