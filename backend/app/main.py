from fastapi import FastAPI,Depends
from .database import Base, engine
from sqlalchemy.orm import Session
from .database import get_db
from .database import SessionLocal
from sqlalchemy import text
from app.models import user
from app.models.user import User
from app.schemas.user_schema import UserRegistration
from app.utils.security import hash_password
from fastapi import HTTPException, status
from app.utils.security import verify_password, create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.schemas.user_schema import UserLogin
from app.utils.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
    
@app.get("/")
#depends(get_db) is used to inject the database session into the endpoint function...
#execute() is used to execute a raw SQL query against the database...

def test_db(db: SessionLocal = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"message": "Database connection successful", "result": result.scalar()}
@app.get("/users")
def get_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return users

# The register_user endpoint is responsible for handling user registration requests.
#  It checks if the email is already registered, hashes the password, and creates a new user in the database. 
# If any errors occur during the process... it rolls back the transaction and returns an appropriate error message.

@app.post("/register")
def register_user(user: UserRegistration, db: SessionLocal = Depends(get_db)):
    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user.password:
         if len(user.password) < 6 or len(user.password) > 72:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be between 6 and 72 characters")
    if user.college_tier is not None:
        if user.college_tier < 1 or user.college_tier > 3:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="College tier must be between 1 and 3")
    # Hash the password before storing it in the database
    hashed_password = hash_password(user.password)
    # Create a new user instance and save it to the database
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        college_tier=user.college_tier
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/auth/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
    
