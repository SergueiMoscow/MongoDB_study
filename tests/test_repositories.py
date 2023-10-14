import pytest

from api.schemas.product import CreateProduct
from repositories.products import ProductRepository
from repositories.users import UserRepository
from tests.conftest import LEN_TEST_PRODUCTS


@pytest.mark.usefixtures('db_for_test')
def test_create_and_read_product(product):
    created_product = product()
    created = ProductRepository.create(created_product)
    assert created.acknowledged
    read_product = ProductRepository.get_by_id(created.inserted_id)
    assert read_product.category == created_product.category
    assert read_product.name == created_product.name
    assert read_product.price == created_product.price


@pytest.mark.usefixtures('db_for_test', 'created_multiple_products')
def test_list_product():
    products_list = ProductRepository.get_all()
    assert len(products_list) == LEN_TEST_PRODUCTS


def test_update_product(product):
    created_product = ProductRepository.create(product())
    updated_product = product()
    ProductRepository.update(
        created_product.inserted_id,
        updated_product,
    )
    read_product = ProductRepository.get_by_id(created_product.inserted_id)
    assert read_product.name == updated_product.name
    assert read_product.category == updated_product.category
    assert read_product.price == updated_product.price


@pytest.mark.usefixtures('db_for_test')
def test_create_and_read_user(user):
    new_user = user()
    created_record = UserRepository.create(new_user)
    assert created_record.acknowledged
    read_record = UserRepository.get_by_id(created_record.inserted_id)
    assert read_record.login == new_user.login
    assert read_record.name == new_user.name
    assert read_record.password == new_user.password
