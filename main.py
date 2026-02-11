from fastapi import FastAPI
from src.users.routes import router as user_router
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router as tag_router
from src.db.database import init_db
from src.errors import register_error_handlers
from src.middleware import register_middleware
app = FastAPI()


register_error_handlers(app)
register_middleware(app)

@app.on_event("startup")
def on_startup():
    init_db()
app.include_router(user_router)
app.include_router(book_router)
app.include_router(auth_router)
app.include_router(review_router)
app.include_router(tag_router)
