from typing import Annotated

from fastapi import APIRouter, Body, Depends

from api.schemas.common import Pagination
from api.schemas.product import CreateProduct, CreateProductResponse, ProductsResponse
from services import services

router = APIRouter()
router.prefix = '/products'


@router.post('/product')
async def post_product(
    product: Annotated[
        CreateProduct,
        Body(
            examples=[
                {
                    'name': 'Apple',
                    'category': 'Food',
                    'price': 99.8,
                }
            ],
            embed=True,
        ),
    ]
) -> CreateProductResponse:
    return await services.create_product(product)


@router.get('/')
async def get_all_products(pagination: Pagination = Depends()) -> ProductsResponse:
    page, limit, products = await services.get_all_products(pagination.page, pagination.limit)
    return ProductsResponse(
        page=page,
        limit=limit,
        result=products,
    )


@router.get('/{product_id}')
async def get_product(product_id: str):
    return await services.get_product_by_id(product_id)
