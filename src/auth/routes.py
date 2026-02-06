from fastapi import APIRouter, Depends, status
from .service import UserService
from src.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.auth.utils import create_access_token, REFRESH_TOKEN_EXPIRY, verify_password
from datetime import timedelta
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)

@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password_hash = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password_hash, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )