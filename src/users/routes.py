from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from src.db.database import get_session
from src.users.schemas import UserCreate, UserUpdate, UserResponse
from src.users.users_db import create_user, get_users, update_user, delete_user
from fastapi import status

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(session, user)


@router.get("/", response_model=List[UserResponse])
def get_users_route(session: Session = Depends(get_session)):
    return get_users(session)


@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: str, user: UserUpdate, session: Session = Depends(get_session)):
    updated_user = update_user(session, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user_route(user_id: str, session: Session = Depends(get_session)):
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
