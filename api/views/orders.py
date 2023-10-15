from typing import Annotated

from fastapi import APIRouter, Body, Depends
from starlette.requests import Request

from api.schemas.common import Pagination, ResponseModel, check_object_id
from api.schemas.order import CreateOrder, CreateOrderResponse, OrderResponse, OrderRequest
from services.orders import OrderService

router = APIRouter()
router.prefix = '/orders'


@router.post('/order')
async def post_order(
    order: Annotated[
        CreateOrder,
        Body(embed=True),
    ]
) -> CreateOrderResponse:
    valid_order = await OrderService.validate(order)
    new_id = await OrderService.create(valid_order)
    return CreateOrderResponse(new_order=new_id)


@router.get('/')
async def get_all_orders(
        pagination: Pagination = Depends(),
        params: OrderRequest = Depends(),
) -> OrderResponse:
    # page, limit, orders = await OrderService.get_all(pagination.page, pagination.limit)
    page, limit, orders = await OrderService.get_custom(pagination, params)
    return OrderResponse(
        page=page,
        limit=limit,
        result=orders,
    )


@router.get('/{order_id}')
async def get_order(order_id: str):
    if check_object_id(order_id):
        return await OrderService.get_by_id(order_id)


@router.patch('/{order_id}')
async def update_order(order_id: str, order: CreateOrder = Body()) -> ResponseModel:
    result = await OrderService.update(order_id, order)
    return result


@router.delete('/{order_id}')
async def delete_order(order_id: str) -> ResponseModel:
    return await OrderService.delete(order_id)
