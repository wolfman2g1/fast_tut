from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from src.api import schemas
from src.api import models
from src.api.database import get_db

router = APIRouter(
    prefix="/posts", tags=["posts"]
)


@router.get("/", response_model=List[schemas.Response])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    db.delete(post)
    db.commit()


@router.put("/{id}", response_model=schemas.Response)
def update_post(id: int, update: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    post_query.update(update.dict())
    db.commit()
    return post_query.first()
