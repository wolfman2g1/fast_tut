from fastapi import FastAPI
from src.api.routers import user,post
import uvicorn


from src.api import models
from src.api.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
uvicorn.run(app)

# test endpoint
@app.get("/ping")
def pong():
    return {"message": "PONG!"}




