from fastapi import APIRouter
from view_model import TableViewModel
from model import TableModel
from database import read_db, write_db
from utils import generate_str_uuid

router = APIRouter(prefix="/table", tags=['Table'])

@router.post("/register")
def register_table(table_view_model: TableViewModel):
    database = read_db()

    table_model = wrapper_table_model(table_view_model)    

    database["tables"][table_model.id] = {
        "capacity" : table_model.capacity, 
        "status" : table_model.status
    }

    write_db(database)

    return {"Mensagem" : "Mesa registrada com sucesso."}

def wrapper_table_model(table: TableViewModel) -> TableModel:
    id = generate_str_uuid()
    return TableModel(
        id=id, 
        capacity=table.capacity, 
        status=table.status
    )
