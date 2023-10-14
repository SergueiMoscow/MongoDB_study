from typing import Any, Optional

from fastapi import HTTPException
from pydantic import BaseModel, model_validator
from starlette import status

PER_PAGE = 10


class Pagination(BaseModel):
    page: Optional[int] = None
    limit: int

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
