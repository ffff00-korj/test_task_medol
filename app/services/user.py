from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.auth.utils import decode_token, generate_token, hash_password, verify_password
from app.infra.postgres.db import GetSessionDep
from app.infra.postgres.models.user import UserModel
from app.infra.postgres.storage.user import UserStorage
from app.schemas.auth import LoginSchema, TokenSchema
from app.schemas.user import UserCreateSchema, UserResponseSchema


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_storage = UserStorage(session)

    async def create(self, user: UserCreateSchema) -> UserResponseSchema:
        user = user.copy()
        user.password = hash_password(user.password)
        try:
            new_user = await self.user_storage.create(UserModel(**user.dict()))
        except IntegrityError as e:
            raise UserAlreadyExistsError from e
        return UserResponseSchema.validate(
            {
                'id': new_user.id,
                'name': new_user.name,
                'role': new_user.role,
            }
        )

    async def login(self, login_form: LoginSchema) -> TokenSchema:
        user = await self.user_storage.get(login_form.name)
        if not user:
            raise UserNotFoundError
        if not verify_password(login_form.password, user.password):
            raise InvalidCredentialsError
        token = generate_token(user.id, user.name, user.role)
        return TokenSchema(token_type='access', access_token=token)

    async def get_from_token(self, token: str) -> UserResponseSchema:
        payload = decode_token(token)
        return UserResponseSchema.validate(
            {
                'id': int(payload['sub']),
                'name': payload['name'],
                'role': payload['role'],
            }
        )


async def get_service(session: GetSessionDep) -> AsyncIterator[UserService]:
    yield UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_service)]
