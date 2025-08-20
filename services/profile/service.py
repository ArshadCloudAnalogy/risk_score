from models.models import User
from models.schema import UserResponse


class ProfileService:

    @staticmethod
    def me(user: User):
        return UserResponse.from_orm(user)

