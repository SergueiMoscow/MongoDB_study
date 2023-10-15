from api.schemas.common import PER_PAGE, ResponseModel
from api.schemas.product import CreateProduct, CreateProductResponse, Product
from repositories.products import ProductRepository
from services.common import CommonService


class ProductService(CommonService):
    _model = Product
    _repository = ProductRepository
    _create_model = CreateProduct
    _create_response_model = CreateProductResponse
    _verbose_name = 'product'
