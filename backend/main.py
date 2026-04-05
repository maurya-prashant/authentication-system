from fastapi import FastAPI
from database import Base, engine
import models

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "DB connected successfully!"}


