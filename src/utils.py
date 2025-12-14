from os import getenv
from dotenv import load_dotenv

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional
import chardet


load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 минут для access token
REFRESH_TOKEN_EXPIRE_DAYS = 7     # 7 дней для refresh token
ALGORITHM = "HS256"
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", "secret")
JWT_REFRESH_SECRET_KEY = getenv("JWT_REFRESH_SECRET_KEY", "secret")

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],  # или ["argon2"] или ["sha256_crypt"]
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
    deprecated="auto",
)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
