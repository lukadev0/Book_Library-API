from sqlalchemy import Column, Integer, String, Boolean, Text
from database_con import Base

class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    author = Column (String)
    description = Column(Text, nullable = True)
    available = Column(Boolean, default = True)

