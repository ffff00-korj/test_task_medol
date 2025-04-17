from fastapi import APIRouter, FastAPI

from app.api.auth import router as auth_router
from app.config import settings

app = FastAPI()


api_router = APIRouter(prefix='/api')
api_router.include_router(auth_router, prefix='/auth', tags=['auth'])

app.include_router(api_router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
