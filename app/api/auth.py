from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from app.schemas.auth import LoginSchema, TokenSchema
from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.services.user import UserAlreadyExistsError, UserServiceDep

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
    return await service.login(login_form)


@router.get('/me')
async def me(request: Request, service: UserServiceDep):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return await service.me(token.split(' ')[1])
