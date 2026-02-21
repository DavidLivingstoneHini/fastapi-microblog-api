from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment, default to SQLite for simplicity
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

# Handle SQLite specifically (needs check_same_thread)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """Get database session - to be used in FastAPI dependencies"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
