from fastapi import APIRouter, Depends
from view_model import LoginViewModel
from database import read_db
from hashlib import md5
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import jwt

router = APIRouter(prefix="/login", tags=["Login"])

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("")
def login(login_data: LoginViewModel):

    database = read_db()
    users_dict = dict(database["users"])
    email = login_data.email
    user_dict_found = dict(users_dict.get(email, None))

    if user_dict_found == None: return {"message" : "Dados incorretos, não foi possível efetuar o login!"}
    hashed_password = user_dict_found.get('password')
    plain_password = get_pwd_hash(login_data.password)

    if not verify_password(login_data.password, hashed_password): return {"message" : "Dados incorretos, não foi possível efetuar o login!"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub" : user_dict_found.get("email")}, expires_delta=access_token_expires)
    return {"message" : "Login efetuado com sucesso.", "token" : Token(access_token=access_token, token_type="bearer")}

def get_pwd_hash(pwd):
    return password_hash.hash(pwd)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
