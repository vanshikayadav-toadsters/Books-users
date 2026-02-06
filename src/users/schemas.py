from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    uid: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True