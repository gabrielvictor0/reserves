from fastapi import APIRouter, Depends, HTTPException, status
from view_model import LoginViewModel
from database import read_db
from hashlib import md5
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    database = read_db()
    users_dict = dict(database["users"])
    email = form_data.username
    user_found = users_dict.get(email, None)

    if user_found == None: raise HTTPException(status_code=400, detail="Email ou senha incorreto.")
    user_dict_found = dict(user_found)
    hashed_password = user_dict_found.get('password')
    # plain_password = get_pwd_hash(form_data.password)

    if not verify_password(form_data.password, hashed_password): raise HTTPException(status_code=400, detail="Email ou senha incorreto.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub" : user_dict_found.get("email")}, expires_delta=access_token_expires)
    return {"message" : "Login efetuado com sucesso.", "token" : Token(access_token=access_token, token_type="bearer")}

# def get_pwd_hash(pwd):
#     return password_hash.hash(pwd)

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
