from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    available: bool = True

    
    class Config:
        from_attributes = True  # Per SQLAlchemy compatibility