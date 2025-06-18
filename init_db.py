
from database_con import engine
from models import Base

def init_database():
  
    print("Creazione tabelle nel database...")
    Base.metadata.create_all(bind=engine)
    print("Tabelle create con successo!")

def drop_all_tables():
  
    print("ATTENZIONE: Eliminazione di tutte le tabelle...")
    Base.metadata.drop_all(bind=engine)
    print("Tabelle eliminate!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_all_tables()
        init_database()
    else:
        init_database()