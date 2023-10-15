import pytest

from repositories.users import UserRepository
from tests.conftest import LEN_TEST_MULTIPLE_RECORDS


@pytest.mark.usefixtures('db_for_test', 'created_multiple_users')
def test_list_users():
    users_list = UserRepository.get_all()
    assert len(users_list) == LEN_TEST_MULTIPLE_RECORDS


@pytest.mark.usefixtures('db_for_test')
def test_create_and_read_user(create_user):
    new_user = create_user()
    created_record = UserRepository.create(new_user.model_dump())
    assert created_record.acknowledged
    read_record = UserRepository.get_by_id(created_record.inserted_id)
    assert read_record.login == new_user.login
    assert read_record.name == new_user.name
    assert read_record.password == new_user.password


@pytest.mark.usefixtures('db_for_test')
def test_update_user(user):
    created_user = UserRepository.create(user().model_dump())
    updated_user = user()
    UserRepository.update(
        created_user.inserted_id,
        updated_user,
    )
    read_product = UserRepository.get_by_id(created_user.inserted_id)
    assert read_product.name == updated_user.name
    assert read_product.password == updated_user.password
    assert read_product.login == updated_user.login


@pytest.mark.usefixtures('db_for_test')
def test_delete_user(create_user):
    new_user = create_user()
    created_user = UserRepository.create(new_user.model_dump())
    inserted_id = created_user.inserted_id
    deleted_user = UserRepository.delete(inserted_id)
    assert deleted_user == 1
