import time
from enum import Enum
from typing import Any

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field, model_validator
from starlette import status

from api.schemas.common import PER_PAGE, ObjectIDModel


class CreateOrderItem(BaseModel):
    product_id: str | None = None
    product_name: str | None = None
    quantity: float | None = Field(default=1.0, ge=0.1)
    price: float | None = Field(default=None, description='Цена')

    @model_validator(mode='before')
    @classmethod
    def product_name_or_id(cls, data: Any):
        if data.get('product_id') is None and data.get('product_name') is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Item must have product name or id',
            )
        return data


class CreateOrder(BaseModel):
    user_id: str | None = Field(default=None, description='ID пользователя')
    user_name: str | None = Field(default=None, description='Имя пользователя')
    items: list[CreateOrderItem] = []
    created: int | float = int(time.time())

    @model_validator(mode='before')
    @classmethod
    def product_name_or_id(cls, data: Any):
        if data.get('user_id') is None and data.get('user_name') is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User must have user_name or user_id',
            )
        return data


class OrderItem(CreateOrderItem):
    price: float = Field(..., ge=0.1)
    amount: float = Field(..., ge=0.1)


class Order(CreateOrder, ObjectIDModel):
    total: float = Field(default=0, ge=0)


class CreateOrderResponse(BaseModel):
    new_order: str


class OrderResponse(BaseModel):
    page: int = 1
    limit: int = PER_PAGE
    result: list[Order]


class OrderSortRequest(Enum):
    DATE: str = 'created'
    USER_ID: str = 'user_id'
    USER_NAME: str = 'user_name'


class Sorting(Enum):
    ASC: str = 'asc'
    DESC: str = 'desc'


class OrderRequest(BaseModel):
    user_id: str | None = None
    user_name: str | None = None
    product_id: str | None = None
    product_name: str | None = None
    date_from: int | None = None
    date_to: int | None = None
    sort_by: OrderSortRequest | None = None
    sorting: Sorting = Query(default=Sorting.ASC)
