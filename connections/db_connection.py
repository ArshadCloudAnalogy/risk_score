from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load from env or hardcoded fallback
DB_USER = os.getenv("POSTGRES_USER", "neondb_owner")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "npg_Rw7GUMrs0Nkv")
DB_HOST = os.getenv("POSTGRES_HOST", "ep-quiet-violet-adqmndog-pooler.c-2.us-east-1.aws.neon.tech")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "neondb")

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
