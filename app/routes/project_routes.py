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


@router.get("/{project_id}", response_model=schemas.Project)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project_by_id(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id={project_id} was not found")
    return project


@router.get("", response_model=List[schemas.Project])
async def get_all_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@router.post("", response_model=schemas.Project)
async def add_project(request: Request, project: schemas.ProjectBase, db: Session = Depends(get_db)):
    project = crud.create_project(db, project=project)
    projects = crud.get_projects(db=db)
    await request.app.project_queue.put(projects)
    return project


@router.put("/{project_id}", response_model=schemas.Project)
async def update_project(request: Request, project_id: int, project: schemas.ProjectBase, db: Session = Depends(get_db)):
    project = crud.update_project(db, project_id=project_id, project=project)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id={project_id} was not found")
    projects = crud.get_projects(db=db)
    await request.app.project_queue.put(projects)
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = crud.delete_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id={project_id} was not found")
    projects = crud.get_projects(db=db)
    tasks = crud.get_tasks(db=db)
    await request.app.task_queue.put(tasks)
    await request.app.project_queue.put(projects)
