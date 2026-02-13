from fastapi import FastAPI
from routes import reserve, table, user, login
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reserve.router)
app.include_router(user.router)
app.include_router(table.router)
app.include_router(login.router)



