from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from src.books.models import Book
from src.books.schemas import BookCreate, BookUpdate


class BookService:
    """Service class for all book-related operations"""
    
    def create_book(self, session: Session, book_data: BookCreate) -> Book:
        """Create a new book"""
        book = Book(**book_data.dict())
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    
    def get_all_books(self, session: Session) -> List[Book]:
        """Get all books"""
        statement = select(Book)
        return session.exec(statement).all()
    
    def get_book_by_id(self, session: Session, book_id: str) -> Optional[Book]:
        """Get a single book by ID"""
        return session.get(Book, book_id)
    
    def update_book(self, session: Session, book_id: str, book_data: BookUpdate) -> Book:
        """Update an existing book"""
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        for key, value in book_data.dict(exclude_unset=True).items():
            setattr(book, key, value)
        
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    
    def delete_book(self, session: Session, book_id: str) -> dict:
        """Delete a book"""
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        session.delete(book)
        session.commit()
        return {"message": "Book deleted successfully"}
    
    def search_books(self, session: Session, query: str) -> List[Book]:
        """Search books by title or author"""
        statement = select(Book).where(
            Book.title.contains(query) | Book.author.contains(query)
        )
        return session.exec(statement).all()
    
    def get_books_by_author(self, session: Session, author: str) -> List[Book]:
        """Get all books by a specific author"""
        statement = select(Book).where(Book.author == author)
        return session.exec(statement).all()
    
    def get_books_by_genre(self, session: Session, genre: str) -> List[Book]:
        """Get all books by genre"""
        statement = select(Book).where(Book.genre == genre)
        return session.exec(statement).all()
    
    def get_book_count(self, session: Session) -> int:
        """Get total number of books"""
        statement = select(Book)
        result = session.exec(statement)
        return len(result.all())
    
    def get_books_by_price_range(self, session: Session, min_price: float, max_price: float) -> List[Book]:
        """Get books within a price range"""
        statement = select(Book).where(
            Book.price >= min_price, 
            Book.price <= max_price
        )
        return session.exec(statement).all()


# Create a singleton instance for easy import
book_service = BookService()

