from celery_app import celery
from datetime import datetime
from schemas import Book
import os

@celery.task
def log_created_book(book_data: dict):
   book = Book(**book_data)
   
   logs_dir = "logs"
   os.makedirs(logs_dir, exist_ok=True)
   log_path = os.path.join(logs_dir, "created_books.log")
   
   with open(log_path, "a") as log_file:
      log_file.write(f"Libro: {book.title} creato alle {datetime.now()}\n")

@celery.task
def delete_book_after_delay(book_id: int):
    
   logs_dir = "logs"
   os.makedirs(logs_dir, exist_ok=True)
   log_path = os.path.join(logs_dir, "deleted_book_request.log")
    
   with open(log_path, "a") as log_file:
      log_file.write(f"Richiesta cancellazione libro con ID {book_id} alle {datetime.now()}\n")