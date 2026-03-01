from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    email=Column(String(100),unique=True,nullable=False,index=True)
    password_hash=Column(String,nullable=False)
    college_tier=Column(Integer)
    created_at=Column(DateTime,default=datetime.utcnow)
    

