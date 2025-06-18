from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from database_con import get_db, engine
from models import BookDB
from schemas import Book
from tasks.book_tasks import log_created_book, delete_book_after_delay
import models

# Crea le tabelle nel database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
api_key_header = APIKeyHeader(name="api_token")
TOKEN = "test_token"

# Dipendenza per verificare il token
def verify_token(api_token: str = Security(api_key_header)):
    if api_token != TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def welcome_message():
    return {"message": "Welcome to the library, choose a book!"}

@app.post("/books", response_model=Book, dependencies=[Security(verify_token)])
async def create_book(book: Book, db: Session = Depends(get_db)):
    db_book = BookDB(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    
    log_created_book.delay(book.dict(), db_book.id)
    
    return db_book

@app.get("/books", response_model=list[Book])
async def get_books(db: Session = Depends(get_db)):
    books = db.query(BookDB).all()
    return books

@app.get("/search/", response_model=list[Book])
async def search_book(title: str, db: Session = Depends(get_db)):
    found_books = db.query(BookDB).filter(
        BookDB.title.ilike(f"%{title}%")
    ).all()
    return found_books

@app.delete("/books/{book_id}", dependencies=[Security(verify_token)])
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    

    delete_book_after_delay.apply_async(args=[book_id, book.title], countdown=5)
    
    db.delete(book)
    db.commit()
    
    return {"message": f"Libro {book_id} eliminato e schedulato per il log di cancellazione tra 5 secondi."}

@app.put("/books/{book_id}", response_model=Book, dependencies=[Security(verify_token)])
async def update_book(book_id: int, updated_book: Book, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    
    db.commit()
    db.refresh(book)
    return book

@app.patch("/books/{book_id}/toggle", response_model=Book, dependencies=[Security(verify_token)])
async def toggle_availability(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.available = not book.available
    db.commit()
    db.refresh(book)
    return book

@app.get("/books/", response_model=list[Book])
async def get_books_from_availability(available: bool, db: Session = Depends(get_db)):
    books = db.query(BookDB).filter(BookDB.available == available).all()
    
    if not books:
        raise HTTPException(
            status_code=404, 
            detail="No books found with the specified availability"
        )
    return books