from fastapi import APIRouter,Depends,status,HTTPException

from sqlalchemy.orm import Session
from src.api.database import  get_db
from src.api import schemas, models, utils, oauth2


router = APIRouter( tags=["authentication"])

@router.post("/login")
def login(user_creds: schemas.UserLogin, db: Session = Depends(get_db())):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credentials")
    if not utils.varify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}