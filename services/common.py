from fastapi import HTTPException
from starlette import status

from api.schemas.common import PER_PAGE, ResponseModel
from api.schemas.user import CreateUser, CreateUserResponse, User
from repositories.users import UserRepository


class CommonService:
    _model = User
    _repository = UserRepository
    _create_model = CreateUser
    _create_response_model = CreateUserResponse
    _verbose_name = 'user'

    @classmethod
    async def get_all(cls, page: int = 1, limit: int = PER_PAGE) -> tuple[int, int, list[_model]]:
        result = cls._repository.get_all(page, limit)
        return page, limit, result

    @classmethod
    async def get_by_id(cls, record_id: str) -> _model | HTTPException:
        result = cls._repository.get_by_id(record_id)
        if result:
            return result
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Object not found')

    @classmethod
    async def create(cls, record: _create_model) -> str:
        result = cls._repository.create(record.model_dump())
        return str(result)

    @classmethod
    async def update(cls, record_id: str, record: _create_model) -> ResponseModel:
        result = cls._repository.update(record_id, record)
        if result:
            return ResponseModel(code=200, data='Success', message=f'{cls._verbose_name} updated')
        else:
            return ResponseModel(
                code=500, data='Error', message=f'Error  updating {cls._verbose_name}'
            )

    @classmethod
    async def delete(cls, record_id: str) -> ResponseModel:
        result = cls._repository.delete(record_id)
        if result:
            return ResponseModel(
                code=200,
                data='Success',
                message=f'{cls._verbose_name} {record_id} has been deleted',
            )
        else:
            return ResponseModel(
                code=500, data='Error', message=f'Error  updating {cls._verbose_name} {record_id}'
            )

    @classmethod
    async def get_by_field(cls, field_name: str, field_value: str) -> _model | None:
        return cls._repository.get_by_field(field_name, field_value)
