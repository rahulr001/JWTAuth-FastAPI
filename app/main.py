from fastapi import FastAPI, Request
from sqlalchemy.ext.declarative import declarative_base
from models.user import User
from routers import auth
Base = declarative_base()
app = FastAPI()


app.include_router(auth.router, tags=['v1'], prefix='/api/v1')
