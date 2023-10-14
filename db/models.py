import time
import uuid

from pydantic import BaseModel, Field


# class Product(BaseModel):
#     id: str | None = None
#     name: str
#     category: str
#     price: float
#     created: int | float = int(time.time())


class User:
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    login = Field(
        alias='login',
        description='Логин',
    )
    name = Field(
        alias='username',
        description='Имя пользователя',
    )


class OrderItem:
    product = Field()
    price = Field()
    quantity = Field()
    amount = Field()


class Order:
    user = Field(description='Пользователь')
    items = Field()
    total = Field()
