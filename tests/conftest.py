from typing import List
from fastapi.testclient import TestClient
from api.app import app
import pytest

from api.schemas.product import CreateProduct, ProductResponse
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
def created_multiple_products(faker) -> List[ProductResponse]:
    products = [
        CreateProduct(
            name=faker.unique.name(),
            category=faker.unique.name(),
            price=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
        )
        for _ in range(LEN_TEST_PRODUCTS)
    ]
    result = []
    for product in products:
        new_object_id = ProductRepository.create_product(product).inserted_id
        result.append(ProductResponse(_id=new_object_id, **product.model_dump()))
    return result


@pytest.fixture
def client():
    return TestClient(app)
