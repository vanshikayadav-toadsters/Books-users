# src/models/user.py
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from src.auth.utils import generate_password_hash
from typing import TYPE_CHECKING, List
from sqlmodel import Relationship
from typing import Optional
if TYPE_CHECKING:
    from src.books.models import Book
    from src.db.models import Review




class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            unique=True,
            nullable=False
        )
    )
    first_name: str =Field(max_length=25)
    last_name:  str =Field(max_length=25)
    username: str = Field(nullable=False, unique=True, index=True)
    email: str = Field(nullable=False, unique=True, index=True)
    password_hash: str = Field(nullable=False)

    #adding role
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")

    )

    created_at: datetime = Field(
       sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow)
    )

    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    books:List["Book"] = Relationship(
        back_populates = "user",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    




