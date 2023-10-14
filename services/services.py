from api.schemas.common import PER_PAGE
from api.schemas.product import CreateProduct, CreateProductResponse, ProductResponse
from repositories.products import ProductRepository


async def get_all_products(page: int = 1, limit: int = PER_PAGE) -> tuple[int, int, list[ProductResponse]]:
    products = ProductRepository.get_all_products(page, limit)
    return page, limit, products


async def get_product_by_id(product_id: str) -> ProductResponse:
    return ProductRepository.get_product(product_id)


async def create_product(product: CreateProduct) -> CreateProductResponse:
    result = ProductRepository.create_product(product)
    return CreateProductResponse(new_product=str(result.inserted_id))
