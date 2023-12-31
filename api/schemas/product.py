import time

from pydantic import BaseModel, Field

from api.schemas.common import PER_PAGE, ObjectIDModel


class CreateProduct(BaseModel):
    # id: bson.ObjectId = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(min_length=3, max_length=30)
    category: str = Field(min_length=3, max_length=30)
    price: float = Field(..., ge=1)
    created: int | float = int(time.time())


class CreateProductResponse(BaseModel):
    new_product: str


class Product(CreateProduct, ObjectIDModel):
    # _id: ObjectId
    # id: str | None = None

    # TODO: Вопрос: Почему это не не выдаёт id во фронт?
    @property
    def get_id(self):
        return self._id


class ProductsResponse(BaseModel):
    page: int = 1
    limit: int = PER_PAGE
    result: list[Product]
