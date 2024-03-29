from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from src.api import schemas
from src.api import models
from src.api import oauth2
from src.api.database import get_db


router = APIRouter(
    prefix="/vote", tags=["Vote"]
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user)
        db.add(new_vote)
        db.commit()
        return {"message": "success"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote doesn't exist")
        vote_query.delete()
        db.commit()
        return {"message": "success"}