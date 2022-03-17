from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from src.api import schemas
from src.api import models
from src.api import oauth2
from src.api.database import get_db

router = APIRouter(
    prefix="/posts", tags=["posts"]
)


@router.get("/", response_model=List[schemas.Response])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.constraints(search)).limit(limit).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_posts(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(user_id=current_user, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{id}", response_model=schemas.Response)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to do this")
    post_query.delete()
    db.commit()


@router.put("/{id}", response_model=schemas.Response)
def update_post(id: int, update: schemas.Post, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to do this")
    post_query.update(update.dict())
    db.commit()
    return post_query.first()
