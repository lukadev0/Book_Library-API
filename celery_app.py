from celery import Celery

celery = Celery(
    "book_api",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=['tasks.book_tasks']  # importante per registrare le tasks
)

if __name__ == "__main__":
    celery.start()