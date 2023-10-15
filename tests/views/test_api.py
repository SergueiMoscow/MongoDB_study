from fastapi import status

from api.schemas.common import Pagination
from repositories.users import UserRepository


def test_create_user_without_body(client):
    response = client.post('/users/user')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_user_by_id(client, mocker, create_user):
    new_user = create_user()
    mock_user_repository = mocker.patch.object(
        UserRepository, 'create', return_value='619e8f45ee462d6d876bbdbc'
    )
    model_dump = new_user.model_dump()
    response = client.post('/users/user', json={'user': model_dump})
    assert response.status_code == status.HTTP_200_OK
    mock_user_repository.assert_called_once_with(model_dump)


def test_get_all_users_ok(client, mocker, create_user):
    mock_all_users = mocker.patch.object(UserRepository, 'get_all', return_value=[])
    response = client.get('users/')
    assert response.status_code == status.HTTP_200_OK
    pagination = Pagination(page=1, limit=10)
    mock_all_users.assert_called_once_with(pagination.page, pagination.limit)


def test_get_all_users_bad_request(client, mocker, create_user):
    mock_all_users = mocker.patch.object(UserRepository, 'get_all', return_value=[])
    response = client.get('users/?page=-1')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
