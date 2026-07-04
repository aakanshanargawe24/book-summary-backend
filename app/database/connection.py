from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres.ecjqeiejypgioquovhqk:Aezakminanu%400501@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
book_engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
BookSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=book_engine

)
Base = declarative_base()

def get_book_db():
    db = BookSessionLocal()
    try:
        yield db
    finally:
        db.close()