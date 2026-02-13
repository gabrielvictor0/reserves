from pydantic import BaseModel

class TableModel(BaseModel):
    id: str
    capacity: int
    status: str

class ReserveModel(BaseModel):
    id: str
    date: str
    status: str
    id_table: str
    id_user: str

class UserModel(BaseModel):
    id : str
    name: str
    email: str
    password: str