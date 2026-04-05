from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

# engine → connection to DB
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread":False}
)
# SessionLocal → lets you talk to DB
SessionLocal = sessionmaker(bind=engine)
# Base → used to create tables
Base = declarative_base()




