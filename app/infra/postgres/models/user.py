from sqlalchemy.orm import Mapped, mapped_column

from app.infra.postgres.models.base import Base
from app.schemas.user import UserRole


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    role: Mapped[UserRole]
    password: Mapped[str]
