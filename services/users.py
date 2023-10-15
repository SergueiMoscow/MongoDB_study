from api.schemas.user import CreateUser, CreateUserResponse, User
from repositories.users import UserRepository
from services.common import CommonService


class UserService(CommonService):
    _model = User
    _repository = UserRepository
    _create_model = CreateUser
    _create_response_model = CreateUserResponse
    _verbose_name = 'user'
