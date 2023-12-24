from fastapi import APIRouter, Depends, Request, Form
import schemas
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import project_routes
from utils import get_db

from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")
router = APIRouter()
host_url = "web-api-project.onrender.com"


@router.get("/project", response_class=HTMLResponse)
async def get_project_page(request: Request, db: Session = Depends(get_db)):
    projects = await project_routes.get_all_projects(0, 100, db=db)
    return templates.TemplateResponse("projects/projects.html", {"request": request, "projects": projects, "host_url": host_url})


@router.get("/project/delete/{project_id}", response_class=RedirectResponse)
async def delete_project(request: Request, project_id: int, db: Session = Depends(get_db)):
    await project_routes.delete_project(request, project_id, db=db)
    return RedirectResponse(url="/project", status_code=303)


@router.get("/project/edit/{project_id}", response_class=HTMLResponse)
async def edit_project_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = await project_routes.get_project(project_id, db=db)
    project.start_date = project.start_date.strftime("%Y-%m-%d %H:%M")
    project.end_date = project.end_date.strftime("%Y-%m-%d %H:%M")
    return templates.TemplateResponse("projects/edit_project.html", {"request": request, "project": project})


@router.post("/project/update/{project_id}", response_class=HTMLResponse)
async def update_project(request: Request, project_id: int, db: Session = Depends(get_db),
                         title: str = Form(...), description: str = Form(...), start_date: str = Form(...), end_date: str = Form(...)):
    update_model = schemas.ProjectBase(title=title, description=description, start_date=start_date, end_date=end_date)
    await project_routes.update_project(request, project_id, update_model, db=db)
    return RedirectResponse(url="/project", status_code=303)


@router.get("/create-project", response_class=RedirectResponse)
async def create_project_page(request: Request):
    return templates.TemplateResponse("/projects/create_project.html", {"request": request})


@router.post("/create-project", response_class=HTMLResponse)
async def create_project_page(request: Request, db: Session = Depends(get_db), title: str = Form(...),
                              description: str = Form(...), start_date: str = Form(...), end_date: str = Form(...)):
    project_model = schemas.ProjectBase(title=title, description=description, start_date=start_date, end_date=end_date)
    await project_routes.add_project(request, db=db, project=project_model)
    return RedirectResponse(url="/project", status_code=303)
