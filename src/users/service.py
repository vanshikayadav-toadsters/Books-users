from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.models import User

class UserService:

    
    async def get_user_by_email(
            self,
            email: str,
            session: AsyncSession
    ):
        
        statement = select(User).where(User.email == email)
        result = session.exec(statement)
        user = result.first()

        return user