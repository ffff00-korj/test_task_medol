from collections.abc import AsyncIterator
from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.config import settings
from app.infra.postgres.db import GetSessionDep
from app.infra.postgres.models.user import UserModel
from app.infra.postgres.storage.user import UserStorage
from app.schemas.auth import LoginSchema, TokenSchema
from app.schemas.user import UserCreateSchema, UserResponseSchema


class UserAlreadyExistsError(Exception):
    pass


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_storage = UserStorage(session)

    async def create(self, user: UserCreateSchema) -> UserResponseSchema:
        user = user.copy()
        user.password = self.hash_password(user.password)
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
            raise HTTPException(
                status_code=400,
                detail=f'User with name {login_form.name} not registered',
            )
        if not self.verify_password(login_form.password, user.password):
            raise HTTPException(status_code=401, detail='Invalid password')
        token = self.generate_token(user.id, user.name, user.role)
        return TokenSchema(token_type='access', access_token=token)

    async def me(self, token: str) -> UserResponseSchema:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        return UserResponseSchema.validate(
            {
                'id': int(payload['sub']),
                'name': payload['name'],
                'role': payload['role'],
            }
        )

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def generate_token(self, id: int, name: str, role: str) -> str:
        payload = {
            'sub': str(id),
            'name': name,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=1),
        }
        return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


async def get_service(session: GetSessionDep) -> AsyncIterator[UserService]:
    yield UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_service)]
