from fastapi import FastAPI
from src.api.routers import user, post, ping, auth, vote

#from src.api import config
from src.api import models
from src.api.database import engine



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(ping.router)
app.include_router(auth.router)
app.include_router(vote.router)
