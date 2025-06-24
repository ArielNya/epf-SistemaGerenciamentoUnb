from sqlalchemy import create_engine, Integer, String, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, Mapped

DATABASE_URL = 'sqlite:///./data/unb.db'
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)
class Base(DeclarativeBase):
    pass

def initDb():
    Base.metadata.create_all(bind=engine)    
    print("banco de dados iniciado")

def getDb():
    db = session()
    try:
        yield db
    finally:
        db.close()



if __name__ == "__main__":
    initDb()