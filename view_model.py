from pydantic import BaseModel

class UserViewModel(BaseModel):
    name: str
    email: str
    password: str

class ReserveViewModel(BaseModel):
    date: str
    status: str
    id_table: str
    id_user: str

class TableViewModel(BaseModel):
    capacity: int
    status: str

class LoginViewModel(BaseModel):
    email: str
    password: str