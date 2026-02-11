from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import BookUpdate, BookCreate
from src.books.service import book_service
from src.books.models import Book
from sqlmodel import Session
from src.db.database import get_session
from typing import List
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from sqlmodel.ext.asyncio.session import AsyncSession



#book_service=BookService()
book_router = APIRouter(prefix="/books", tags=["Books"])
acccess_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(allowed_roles=["admin", "user"])
review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED , dependencies=[Depends(RoleChecker)])
def create_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    token_details=Depends(acccess_token_bearer),
) -> dict :
    user_id = token_details["user"]["user_uid"]
    """Create a new book (Protected)"""
    return book_service.create_book(session, book_data, user_id)


@book_router.get("/", response_model=List[Book])
def get_all_books(
    session: Session = Depends(get_session),
    token_details=Depends(acccess_token_bearer),
):
    """Get all books (Protected)"""
    return book_service.get_all_books(session)


@book_router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: str,
    book_data: BookUpdate,
    session: Session = Depends(get_session),
    token_details=Depends(acccess_token_bearer),
):
    """Update a book (Protected)"""
    return book_service.update_book(session, book_id, book_data)


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: str,
    session: Session = Depends(get_session),
    token_details=Depends(acccess_token_bearer),
):
    """Delete a book (Protected)"""
    book_service.delete_book(session, book_id)
    return None