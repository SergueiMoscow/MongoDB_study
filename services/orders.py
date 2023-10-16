from fastapi import HTTPException
from starlette import status

from api.schemas.common import Pagination
from api.schemas.order import (
    CreateOrder,
    CreateOrderItem,
    CreateOrderResponse,
    Order,
    OrderItem,
    OrderRequest,
)
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
        items: [OrderItem] = []
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
            items.append(valid_item)
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

    @classmethod
    async def get_custom(
        cls, pagination: Pagination, params: OrderRequest
    ) -> tuple[int, int, list[_model]]:
        # order_request = {'time': 167803456, 'user_name': 'Alex', 'sort_by': 'time', 'sorting': 'desc'}
        query = {}
        if params.user_name:
            query.update({'user_name': params.user_name})
        if params.user_id:
            query.update({'user_id': params.user_id})
        if params.product_id:
            query.update({'items.product_id': params.product_id})
        if params.product_name:
            query.update({'items.product_name': params.product_name})
        if params.date_from:
            query.update({'created': {'$gte': params.date_from}})
        if params.date_to:
            query.update({'created': {'$lte': params.date_to}})

        result = cls._repository.get_custom(
            pagination, query=query, sort_by=str(params.sort_by.value), sorting=params.sorting
        )
        return pagination.page, pagination.limit, result
