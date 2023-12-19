from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
import crud
import schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{task_id}", response_model=schemas.Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id={task_id} was not found")
    return task


@router.get("", response_model=List[schemas.Task])
async def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.post("", response_model=schemas.Task)
async def create_task(request: Request, task: schemas.CreateTask, db: Session = Depends(get_db)):
    exist_project = crud.get_project_by_id(db, project_id=task.project_id)
    if exist_project:
        task = crud.create_task(db, task=task)
        tasks = crud.get_tasks(db=db)
        await request.app.task_queue.put(tasks)
        return task
    raise HTTPException(status_code=404, detail=f"Project with {task.project_id} was not found")


@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(request: Request, task: schemas.CreateTask, task_id: int, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id=task_id, task=task)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id={task_id} was not found")
    tasks = crud.get_tasks(db=db)
    await request.app.task_queue.put(tasks)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} was not found")
    tasks = crud.get_tasks(db=db)
    await request.app.task_queue.put(tasks)
