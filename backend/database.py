# database.py
# This file sets up the database connection and session management.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The URL that tells SQLAlchemy which database to use.
# "sqlite:///./test.db" means: use SQLite, create a file called test.db in the current folder.
# For production, swap this with PostgreSQL: "postgresql://user:password@localhost/dbname"
DATABASE_URL = "sqlite:///./test.db"

# The engine is the core connection to the database.
# "check_same_thread: False" is SQLite-specific — it allows the same connection
# to be used across multiple threads (needed because FastAPI uses async threads).
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory that creates new database sessions.
# Each request to your API will get its own session (like its own private workspace with the DB).
# autocommit=False → changes are NOT saved automatically, you must call db.commit() manually.
# autoflush=False  → changes are NOT sent to DB before every query automatically.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class for all your database models (tables).
# Every model (like User) will inherit from this Base.
Base = declarative_base()


# This is a FastAPI "dependency" — it's injected into route functions via Depends(get_db).
# It creates a fresh DB session for each request, hands it to the route, 
# then closes it automatically when the request is done (even if an error occurs).
# This prevents memory leaks and connection buildup.
def get_db():
    db = SessionLocal()
    try:
        yield db       # hand the session to whoever called Depends(get_db)
    finally:
        db.close()     # always close, even if an exception was raised