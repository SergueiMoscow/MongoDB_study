from fastapi import HTTPException
from starlette import status

from api.schemas.order import CreateOrder, CreateOrderItem, CreateOrderResponse, Order, OrderItem
from api.schemas.user import User
from repositories.orders import OrderRepository
from services.common import CommonService
from services.products import ProductService
from services.users import UserService


class OrderService(CommonService):
    _model = Order
    _repository = OrderRepository
    _create_model = CreateOrder
    _create_response_model = CreateOrderResponse
    _verbose_name = 'order'

    @classmethod
    async def validate(cls, create_order: CreateOrder) -> Order | None:
        user = await cls.valid_user(create_order)
        items: [dict] = []
        total: float = 0.0
        order_dict = {'user_id': user.id, 'user_name': user.name}
        for item in create_order.items:
            product = await cls.valid_product(item)
            price = item.price if item.price else product.price
            amount = price * item.quantity
            valid_item = OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=item.quantity,
                price=price,
                amount=amount,
            )
            total += amount
            items.append(valid_item.model_dump())
        order_dict['items'] = items
        order_dict['total'] = total
        result = Order(**order_dict)
        return result

    @classmethod
    async def valid_user(cls, create_order: CreateOrder) -> User:
        if create_order.user_id:
            return await UserService.get_by_id(create_order.user_id)
        elif create_order.user_name:
            return await UserService.get_by_field('login', create_order.user_name)
        else:
            raise HTTPException(status_code=400, detail='user_id or user_name must be non null')

    @classmethod
    async def valid_product(cls, product: CreateOrderItem):
        if product.product_id:
            return await ProductService.get_by_id(product.product_id)
        elif product.product_name:
            return await ProductService.get_by_field('name', product.product_name)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='product_id or product_name must be not null',
            )
