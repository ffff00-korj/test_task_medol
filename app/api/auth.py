from fastapi import APIRouter

router = APIRouter()


@router.get('/register')
async def register():
    return {'error': 'Not implemented'}


@router.get('/login')
async def login():
    return {'error': 'Not implemented'}


@router.get('/me')
async def me():
    return {'error': 'Not implemented'}
