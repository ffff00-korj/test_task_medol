from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class AppConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class PostgresConfig(BaseModel):
    host: str = Field(default='localhost', alias='POSTGRES_HOST')
    port: int = Field(default=5432, alias='POSTGRES_PORT')
    name: str = Field(default='db', alias='POSTGRES_DB')
    user: str = Field(default='user', alias='POSTGRES_USER')
    password: str = Field(default='password', alias='POSTGRES_PASSWORD')


class Settings(BaseSettings):
    app: AppConfig = Field(default=AppConfig())
    postgres: PostgresConfig = Field(default=PostgresConfig())

    @property
    def postgres_uri(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres.user}:{self.postgres.password}@'
            f'{self.postgres.host}:{self.postgres.port}/{self.postgres.name}'
        )


settings = Settings()
