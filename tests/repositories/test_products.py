import pytest

from repositories.products import ProductRepository
from tests.conftest import LEN_TEST_MULTIPLE_RECORDS


@pytest.mark.usefixtures('db_for_test')
def test_create_and_read_product(product):
    created_product = product()
    created = ProductRepository.create(created_product.model_dump())
    assert created.acknowledged
    read_product = ProductRepository.get_by_id(created.inserted_id)
    assert read_product.category == created_product.category
    assert read_product.name == created_product.name
    assert read_product.price == created_product.price


@pytest.mark.usefixtures('db_for_test', 'created_multiple_products')
def test_list_product():
    products_list = ProductRepository.get_all()
    assert len(products_list) == LEN_TEST_MULTIPLE_RECORDS


@pytest.mark.usefixtures('db_for_test')
def test_update_product(product):
    created_product = ProductRepository.create(product().model_dump())
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
def test_delete_product(product):
    new_product = product()
    created_product = ProductRepository.create(new_product.model_dump())
    inserted_id = created_product.inserted_id
    deleted_product = ProductRepository.delete(inserted_id)
    assert deleted_product == 1
