from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
import crud
import schemas
from database import SessionLocal, engine

from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    exist_user = crud.get_user(db, user_id=user_id)
    if exist_user is None:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} was not found")
    return exist_user


@router.post("", response_model=schemas.User)
async def create_user(request: Request, user: schemas.UserBase, db: Session = Depends(get_db)):
    exist_user = crud.get_user_by_email(db, email=user.email)
    if exist_user:
        raise HTTPException(status_code=400, detail=f"User with email={user.email} already registered")
    user = crud.create_user(db=db, user=user)
    users = crud.get_users(db)
    await request.app.user_queue.put(users)
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(request: Request, user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id=user_id, user=user)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} was not found")
    users = crud.get_users(db)
    await request.app.user_queue.put(users)
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} was not found")
    users = crud.get_users(db)
    await request.app.user_queue.put(users)
