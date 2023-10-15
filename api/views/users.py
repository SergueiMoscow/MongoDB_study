from typing import Annotated

from fastapi import APIRouter, Body, Depends

from api.schemas.common import Pagination, ResponseModel, check_object_id
from api.schemas.product import CreateProduct, CreateProductResponse, ProductsResponse
from api.schemas.user import CreateUser, UserResponse, CreateUserResponse
from services import products
from services.users import UserService

router = APIRouter()
router.prefix = '/users'


@router.post('/user')
async def post_user(
    user: Annotated[
        CreateUser,
        Body(embed=True),
    ]
) -> CreateUserResponse:
    new_id = await UserService.create(user)
    return CreateUserResponse(new_user=new_id)


@router.get('/')
async def get_all_users(pagination: Pagination = Depends()) -> UserResponse:
    page, limit, users = await UserService.get_all(pagination.page, pagination.limit)
    return UserResponse(
        page=page,
        limit=limit,
        result=users,
    )


@router.get('/{user_id}')
async def get_user(user_id: str):
    if check_object_id(user_id):
        return await UserService.get_by_id(user_id)


@router.patch('/{user_id}')
async def update_user(user_id: str, user: CreateUser = Body()) -> ResponseModel:
    result = await UserService.update(user_id, user)
    return result


@router.delete('/{user_id}')
async def delete_user(user_id: str) -> ResponseModel:
    return await UserService.delete(user_id)
