from pydantic import BaseModel
from typing import List

# Pydantic модели
class UsersCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class TokenResponse(BaseModel):
    message: str
    token_type: str

# Простая модель для хранения
class User:
    def __init__(self, first_name, last_name, email, hashed_password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password

# Хранилища в памяти
fake_users_store: List[User] = []
fake_redis_store = {}

# Заглушки для зависимостей
async def get_db():
    return None

async def get_redis():
    return None

# Алиасы для совместимости
user_schemas = type('obj', (object,), {
    'UsersCreate': UsersCreate
})

auth_schemas = type('obj', (object,), {
    'TokenResponse': TokenResponse
})

Users = User