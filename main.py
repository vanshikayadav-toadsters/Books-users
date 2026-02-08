from fastapi import FastAPI
from src.users.routes import router as user_router
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.db.database import init_db
app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()
app.include_router(user_router)
app.include_router(book_router)
app.include_router(auth_router)
