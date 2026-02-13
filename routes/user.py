from fastapi import APIRouter
from view_model import UserViewModel
from model import UserModel
from hashlib  import md5
from database import read_db, write_db
from utils import generate_str_uuid
from pwdlib import PasswordHash

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register")
def register_user(user_view_model: UserViewModel):

    database = read_db()

    users_dict = dict(database['users'])

    email_exist = verify_email(user_view_model, users_dict)

    if email_exist: return {"message" : "Já existe uma conta com este endereço de E-mail."}

    user_model = wrapper_user_model(user_view_model)

    database["users"][user_model.email] = {
        "id": user_model.id, 
        "email" : user_model.email,
        "name": user_model.name,
        "password": user_model.password
    }

    write_db(database)

    return "Usuário criado com sucesso!"

def verify_email(user_view_model: UserViewModel, users_dict: dict) -> bool:
    if users_dict.get(user_view_model.email, None) != None: return True

def wrapper_user_model(user_view_model: UserViewModel) -> UserModel:
    id = generate_str_uuid()

    hash = PasswordHash.recommended()
    pwd_hash =  hash.hash(user_view_model.password)

    user_json = user_view_model.model_dump()

    return UserModel(id=id, name=user_json["name"], email=user_json["email"], password=pwd_hash)