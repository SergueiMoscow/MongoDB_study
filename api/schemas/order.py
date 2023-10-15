from fastapi import HTTPException
from typing import Any

from pydantic import BaseModel, Field, model_validator
from starlette import status

from api.schemas.common import ObjectIDModel, PER_PAGE


class CreateOrderItem(BaseModel):
    product_id: str | None = None
    product_name: str | None = None
    quantity: float | None = Field(deault=1.0, ge=0.1)
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
