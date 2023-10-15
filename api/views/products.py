from typing import Annotated

from fastapi import APIRouter, Body, Depends

from api.schemas.common import Pagination, ResponseModel, check_object_id
from api.schemas.product import CreateProduct, CreateProductResponse, ProductsResponse
from services import products
from services.products import ProductService

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
    new_id = await ProductService.create(product)
    return CreateProductResponse(new_product=new_id)


@router.get('/')
async def get_all_products(pagination: Pagination = Depends()) -> ProductsResponse:
    page, limit, products = await ProductService.get_all(pagination.page, pagination.limit)
    return ProductsResponse(
        page=page,
        limit=limit,
        result=products,
    )


@router.get('/{product_id}')
async def get_product(product_id: str):
    if check_object_id(product_id):
        return await services.get_product_by_id(product_id)


@router.patch('/{product_id}')
async def update_product(product_id: str, product: CreateProduct = Body()) -> ResponseModel:
    result = await services.update_product(product_id, product)
    return result
