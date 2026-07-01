from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# We encode the '@' in your password to '%40' so the URL parser doesn't break,
# and we strip out '?pgbouncer=true' entirely.
DATABASE_URL = "postgresql://postgres.ecjqeiejypgioquovhqk:Aezakminanu%400501@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()