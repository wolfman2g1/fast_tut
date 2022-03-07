from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from routers import post,user

from sqlalchemy.sql.functions import mode
import schemas
import models
import utils
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


# test endpoint
@app.get("/ping")
def pong():
    return {"message": "PONG!"}




