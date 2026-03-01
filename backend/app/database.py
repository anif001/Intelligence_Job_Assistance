from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:0423@localhost:5432/tech_simulator"

#main connection manager to the database...like a bridge between bg and db
engine = create_engine(DATABASE_URL)
#SessionLocal is used to create new sessions for each request to the database..
# 1. bind=engine: it connects the session to the db...
#2.autocommit=False: it means that changes to the database wont be saved automatically..
#3.autoflush=False: it means that changes to the database wont be flushed automatically..

SessionLocal=sessionmaker( 
    autocommit=False,
    autoflush=False, 
    bind=engine)
#Base:it is a base class for all the models in the applicaqtion...
#declarative_base() is a function that returns a new base class from which all mapped classes should inherit...

Base=declarative_base()

#dependency to get db session for each request...it creates a new session and closes it after the request is done...
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
#yield is used to return a value from a generator function.
# close() is used to close the database session after the request is done...

