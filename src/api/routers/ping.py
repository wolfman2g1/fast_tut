from fastapi import APIRouter

router = APIRouter()
# test endpoint
@router.get("/ping")
def pong():
    return {"message": "PONG!"}