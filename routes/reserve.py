from model import ReserveModel
from view_model import ReserveViewModel
from database import read_db, write_db
from utils import generate_str_uuid
from typing import Annotated
from fastapi import Depends, FastAPI, APIRouter
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/reserve", tags=['Reserve'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/reserve")
def register_reserve(reserve: ReserveViewModel, token: Annotated[str, Depends(oauth2_scheme)]):
    database = read_db()

    new_reserve_model = wrapper_reserve_model(reserve)

    database["reserves"].append(new_reserve_model.model_dump())

    write_db(database)

    return {"message" : "Reserva registrada com sucesso."}
    

def wrapper_reserve_model(reserve: ReserveViewModel) -> ReserveModel:
    id = generate_str_uuid()
    return ReserveModel(
        id=id, date=reserve.date, 
        status=reserve.status,
        id_table=reserve.id_table, 
        id_user=reserve.id_user
    )

