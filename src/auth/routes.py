from fastapi import APIRouter, Depends, status
from .service import UserService
from src.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.auth.utils import create_access_token, REFRESH_TOKEN_EXPIRY, verify_password
from datetime import timedelta ,datetime
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from src.db.redis import add_jti_to_blocklist
from src.auth.dependencies  import AccessTokenBearer, RefreshTokenBearer, RoleChecker
from src.users.schemas import UserResponse
from src.auth.dependencies import get_current_user


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])

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

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )


@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):

    print(f"Token details received: {token_details}")  # Debug line
    
    jti = token_details.get('jti')
    print(f"Extracted JTI: {jti}")  # Debug line

    if jti:
        await add_jti_to_blocklist(jti)
        return JSONResponse(
            content={
                "message":"Logged Out Successfully"
            },
            status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid token format - missing JTI"
        )
    
@auth_router.get("/me", response_model=UserResponse)
async def get_current_user(
    user=Depends(get_current_user)):
    return user