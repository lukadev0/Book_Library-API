from fastapi import FastAPI, HTTPException, Header, Depends, Security
from fastapi.security import APIKeyHeader
from schemas import Book
from tasks.book_tasks import log_created_book, delete_book_after_delay


app = FastAPI()
api_key_header = APIKeyHeader(name = "api_token")
TOKEN = "test_token"
books: list[Book] = []



#dipendenza
def verify_token(api_token: str = Security(api_key_header)):
    if api_token != TOKEN:
        raise HTTPException(status_code = 401, detail = "Invalid token")
    

@app.get("/")
async def welcome_message():
    return {"message": "Welcome to the library, choose a book!"}

@app.post("/books", response_model=Book, dependencies=[Security(verify_token)])
async def create_book(book: Book):
    books.append(book)
    log_created_book(book.dict())
    return book

@app.get("/books", response_model=list[Book])
async def get_books():
    return books    

@app.get("/search/", response_model=list[Book])
async def search_book(title: str ):
   found_book = [book for book in books if title.lower() in book.title.lower()]
   return found_book
    

@app.delete("/books/{book_id}", dependencies=[Security(verify_token)])
async def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            delete_book_after_delay.apply_async(args=[book_id], countdown=5)
            books.remove(book)
            return {"message": f"Libro {book_id} schedulato per il log di cancellazione tra 5 secondi."}
    raise HTTPException(status_code=404, detail="Book not found")



@app.put("/books/{book_id}", response_model=Book, dependencies=[Security(verify_token)])
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code = 404, detail = "Book not found")

@app.patch("/books/{book_id}/toggle", response_model = Book, dependencies=[Security(verify_token)])
async def toggle_availability(book_id: int):
    for book in books: 
        if book.id == book_id:
            book.available = not book.available
            return book 
    raise HTTPException(status_code = 404, detail = "Book not found")


@app.get("/books/", response_model = list[Book])
async def get_books_from_availability(available: bool):
    
    result = []
    
    for book in books:
        if book.available == available:
            result.append(book)
        
    if result == []:
            raise HTTPException(status_code=404, detail="No books found with the specified availability")
    return result






