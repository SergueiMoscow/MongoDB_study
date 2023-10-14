from typing import Any, Optional, Annotated

from bson import ObjectId as _ObjectId
from fastapi import HTTPException
from pydantic import BaseModel, model_validator, AfterValidator
from starlette import status

PER_PAGE = 10


class Pagination(BaseModel):
    page: Optional[int] = None
    limit: int = PER_PAGE

    @model_validator(mode='before')
    @classmethod
    def validate_page(cls, data: Any) -> Any:
        page = data['page']
        if page is None:
            data['page'] = 1
        elif page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='page should be greater than or equal to 1',
            )
        return data


class ResponseModel(BaseModel):
    data: str | None = None
    code: int = 200
    message: str = 'Response'


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise HTTPException(
            status_code=400,
            detail='Invalid ObjectId'
        )
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]


class ObjectIDModel(BaseModel):
    _id: ObjectId
    id: str | None = None

