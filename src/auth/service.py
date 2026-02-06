from src.users.models import User
from src.users.schemas import UserCreate
from sqlmodel import select
from src.auth.utils import generate_password_hash, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = session.exec(statement)

        user = result.first()

        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        
        # Remove password and add password_hash
        password = user_data_dict.pop("password")
        user_data_dict["password_hash"] = generate_password_hash(password)

        new_user = User(**user_data_dict)

        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user
    