from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    product = Field()
    price = Field()
    quantity = Field()
    amount = Field()


class Order(BaseModel):
    user: str = Field(description='Пользователь')
    items: list[OrderItem] = []
    total: float = Field(default=0, ge=0)
