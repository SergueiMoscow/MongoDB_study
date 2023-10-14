import pytest

from api.schemas.product import CreateProduct
from repositories.products import ProductRepository
from tests.conftest import LEN_TEST_PRODUCTS


@pytest.mark.usefixtures('db_for_test')
def test_create_and_read_product():
    product = CreateProduct(name='test', category='cat1', price=100)
    created_product = ProductRepository.create_product(product)
    assert created_product.acknowledged
    read_product = ProductRepository.get_product(created_product.inserted_id)
    assert read_product.category == product.category
    assert read_product.name == product.name
    assert read_product.price == product.price


@pytest.mark.usefixtures('db_for_test', 'created_multiple_products')
def test_list_product():
    products_list = ProductRepository.get_all_products()
    assert len(products_list) == LEN_TEST_PRODUCTS
