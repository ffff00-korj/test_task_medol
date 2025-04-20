from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from app.schemas.auth import LoginSchema, TokenSchema
from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.services.user import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserServiceDep,
)

router = APIRouter()


@router.post('/register')
async def register(
    new_user: UserCreateSchema,
    service: UserServiceDep,
) -> UserResponseSchema:
    try:
        return await service.create(new_user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=400,
            detail=f'User with name {new_user.name} already exists',
        ) from e


@router.post('/login')
async def login(login_form: LoginSchema, service: UserServiceDep) -> TokenSchema:
    try:
        return await service.login(login_form)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail=f'User with name {login_form.name} not registered',
        ) from e
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail='Invalid password') from e


@router.get('/me')
async def me(request: Request, service: UserServiceDep):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return await service.get_from_token(token.split(' ')[1])
