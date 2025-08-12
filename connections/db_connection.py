from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load from env or hardcoded fallback
DB_USER = os.getenv("POSTGRES_USER", "neondb")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "riskcore_db")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "riskcore_db")
# psql 'postgresql://neondb_owner:npg_7Yb1tpICxvdQ@ep-damp-dream-a1fv7xe6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
