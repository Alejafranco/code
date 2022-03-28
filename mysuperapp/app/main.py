from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from . import db, models
from .api import items, users


def create_db_and_tables():
    assert models, "Models should be imported so SQLModel has them registered"
    SQLModel.metadata.create_all(db.engine)


app = FastAPI(
    title="My Super App",
    version="0.3.0",
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://fastapiworkshop.yaquelinehoyos.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, tags=["users"])
app.include_router(items.router, tags=["items"])


@app.on_event("startup")
def startup_event():
    create_db_and_tables()