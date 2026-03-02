from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",

)
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# hash_password() takes a plain text password and returns a hashed version of it using the bcrypt algorithm.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
#verify_password() takes a plain text password and a hashed password, and returns True if the plain text password matches the hashed password, 
# otherwise it returns False.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# create_access_token() takes a dictionary of data and an optional expiration time...
#  and returns a JSON Web Token (JWT) that encodes the data along with the expiration time.
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt