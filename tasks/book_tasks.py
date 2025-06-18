from celery_app import celery
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:bookuser@pass:5432/book_library"
)

# Engine e session factory per i task
task_engine = create_engine(DATABASE_URL)
TaskSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=task_engine)

@celery.task
def log_created_book(book_data: dict, book_id: int):
    try:
        
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        log_path = os.path.join(logs_dir, "created_books.log")
        

        with open(log_path, "a") as log_file:
            log_file.write(
                f"Libro ID {book_id}: '{book_data['title']}' di {book_data['author']} "
                f"creato alle {datetime.now()}\n"
            )
        
        print(f"Log creazione libro completato per ID {book_id}")
        
    except Exception as e:
        print(f"Errore nel task log_created_book: {e}")
       

@celery.task
def delete_book_after_delay(book_id: int, book_title: str):

    try:
       
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        log_path = os.path.join(logs_dir, "deleted_book_request.log")
        
        g
        with open(log_path, "a") as log_file:
            log_file.write(
                f"Richiesta cancellazione completata - Libro ID {book_id} "
                f"'{book_title}' cancellato alle {datetime.now()}\n"
            )
        
        print(f"Log cancellazione libro completato per ID {book_id}")
        
    except Exception as e:
        print(f"Errore nel task delete_book_after_delay: {e}")


'''@celery.task  // Task opzionale per pulizia periodica dei vecchi log con celery beat
def cleanup_old_logs():
    try:
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            return "Nessuna directory logs da pulire"
        
        # Logica per cleanup (esempio: file più vecchi di 30 giorni)
        # Implementazione specifica dipende dai requisiti
        
        return "Cleanup completato"
        
    except Exception as e:
        print(f"Errore nel cleanup: {e}")
        return f"Errore nel cleanup: {e}"'''