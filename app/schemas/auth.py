from pydantic import BaseModel


class LoginSchema(BaseModel):
    name: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
