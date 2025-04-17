from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = '0.0.0.0'
    app_port: int = 8000

    db_host: str = Field(default='db', alias='POSTGRES_HOST')
    db_port: int = Field(default=5432, alias='POSTGRES_PORT')
    db_name: str = Field(default='db', alias='POSTGRES_DB')
    db_user: str = Field(default='user', alias='POSTGRES_USER')
    db_password: str = Field(default='password', alias='POSTGRES_PASSWORD')


settings = Settings()
