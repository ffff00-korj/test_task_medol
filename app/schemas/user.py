from enum import Enum


class UserRole(str, Enum):
    USER = 'patient'
    DOCTOR = 'doctor'
    ADMIN = 'admin'
