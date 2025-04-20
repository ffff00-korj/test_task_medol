from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    patient = 'patient'
    doctor = 'doctor'
    admin = 'admin'


class UserSchema(BaseModel):
    name: str
    role: UserRole


class UserCreateSchema(UserSchema):
    password: str


class UserResponseSchema(UserSchema):
    id: int
    name: str
    role: UserRole
