from fastapi import APIRouter, Depends, Request, Form
import schemas
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import project_routes, task_routes
from utils import get_db

from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")
router = APIRouter()

host_url = "web-api-project.onrender.com"


@router.get("/task")
async def get_user_page(request: Request, db: Session = Depends(get_db)):
    tasks = await task_routes.get_tasks(0, 1000, db=db)
    return templates.TemplateResponse("task/task.html", {"request": request, "tasks": tasks, "host_url": host_url})


@router.get("/task/delete/{task_id}", response_class=RedirectResponse)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    await task_routes.delete_task(request, task_id, db=db)
    return RedirectResponse(url="/task", status_code=303)


@router.get("/create-task", response_class=HTMLResponse)
async def create_task_page(request: Request, db: Session = Depends(get_db)):
    projects = await project_routes.get_all_projects(0, 1000, db=db)
    return templates.TemplateResponse("task/create_task.html", {"request": request, "projects": projects})


@router.post("/create-task", response_class=RedirectResponse)
async def create_task(request: Request, db: Session = Depends(get_db), title: str = Form(...), description: str = Form(...),
                      status: str = Form(...), created_at: str = Form(...), due_date: str = Form(...), project_id: str = Form(...)):
    new_task = schemas.CreateTask(
        title=title, description=description, status=status,
        created_at=created_at, due_date=due_date, project_id=project_id
    )
    await task_routes.create_task(request, new_task, db=db)
    return RedirectResponse(url="/task", status_code=303)


@router.get("/task/edit/{task_id}", response_class=HTMLResponse)
async def edit_task_page(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = await task_routes.get_task(task_id, db=db)
    task.created_at = task.created_at.strftime("%Y-%m-%d %H:%M")
    task.due_date = task.due_date.strftime("%Y-%m-%d %H:%M")
    projects = await project_routes.get_all_projects(0, 100, db=db)
    return templates.TemplateResponse("task/edit_task.html",
                                      {"request": request, "projects": projects, "task": task})


@router.post("/task/update/{task_id}", response_class=RedirectResponse)
async def update_task(request: Request, task_id: int, db: Session = Depends(get_db), title: str = Form(...), description: str = Form(...),
                      status: str = Form(...), created_at: str = Form(...), due_date: str = Form(...),
                      project_id: str = Form(...)):
    update_model = schemas.CreateTask(
        title=title, description=description, status=status,
        created_at=created_at, due_date=due_date, project_id=project_id
    )
    await task_routes.update_task(request, task_id=task_id, task=update_model, db=db)
    return RedirectResponse(url="/task", status_code=303)
