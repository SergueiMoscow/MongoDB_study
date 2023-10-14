from api.schemas.common import PER_PAGE, ResponseModel
from api.schemas.product import CreateProduct, CreateProductResponse, Product
from repositories.products import ProductRepository


async def get_all_products(page: int = 1, limit: int = PER_PAGE) -> tuple[int, int, list[Product]]:
    products = ProductRepository.get_all(page, limit)
    return page, limit, products


async def get_product_by_id(product_id: str) -> Product:
    return ProductRepository.get_by_id(product_id)


async def create_product(product: CreateProduct) -> CreateProductResponse:
    result = ProductRepository.create(product)
    return CreateProductResponse(new_product=str(result.inserted_id))


async def update_product(product_id: str, product: CreateProduct) -> ResponseModel:
    result = ProductRepository.update(product_id, product)
    if result:
        return ResponseModel(
            code=200,
            data='Success',
            message='Product updated'
        )
    else:
        return ResponseModel(
            code=500,
            data='Error',
            message='Error  updating product'
        )
