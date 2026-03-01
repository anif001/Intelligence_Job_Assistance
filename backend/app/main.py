from fastapi import FastAPI,Depends
from .database import engine
from sqlalchemy.orm import Session

from .database import get_db
from .database import SessionLocal
from sqlalchemy import text



app = FastAPI()
@app.get("/")
def test_db(db: SessionLocal = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"message": "Database connection successful", "result": result.scalar()}
    
