from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.db.database import get_session
from src.books.schemas import BookCreate, BookUpdate
from src.books.books_db import create_book, get_books, update_book, delete_book
from src.auth.dependencies import AccessToken

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/")
def create_book_route(book: BookCreate, session: Session = Depends(get_session)):
    return create_book(session, book)


@router.get("/")
def get_books_route(session: Session = Depends(get_session)):
    return get_books(session)


@router.put("/{book_id}")
def update_book_route(book_id: str, book: BookUpdate, session: Session = Depends(get_session)):
    updated_book = update_book(session, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/{book_id}")
def delete_book_route(book_id: str, session: Session = Depends(get_session)):
    success = delete_book(session, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}

