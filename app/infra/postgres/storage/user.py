from sqlalchemy import select

from app.infra.postgres.models import UserModel


class UserStorage:
    def __init__(self, session):
        self.session = session

    async def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        await self.session.commit()
        return user

    async def get(self, name: str) -> UserModel:
        query = select(UserModel).where(UserModel.name == name)
        user = await self.session.execute(query)
        return user.scalars().first()
