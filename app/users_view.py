from fastapi import APIRouter, Depends, Request, Form
import schemas
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import user_routes
from utils import get_db

from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")
router = APIRouter()
host_url = "web-api-project.onrender.com"


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "message": "Hello!!!!"})


@router.get("/user")
async def get_user_page(request: Request, db: Session = Depends(get_db)):
    users = await user_routes.read_users(0, 100, db=db)
    return templates.TemplateResponse("users/users.html", {"request": request, "users": users, "host_url": host_url})


@router.get("/user/delete/{user_id}", response_class=RedirectResponse)
async def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    await user_routes.delete_user(request, user_id, db=db)
    return RedirectResponse(url="/user")


@router.get("/create-user", response_class=HTMLResponse)
async def get_create_user(request: Request):
    return templates.TemplateResponse("users/create_user.html", {"request": request})


@router.post("/create-user", response_class=RedirectResponse)
async def create_user(request: Request, db: Session = Depends(get_db), name: str = Form(...), email: str = Form(...)):
    await user_routes.create_user(request, schemas.UserBase(name=name, email=email), db=db)
    return RedirectResponse(url="/user", status_code=303)


@router.get("/user/edit/{user_id}")
async def get_update_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = await user_routes.get_user_by_id(user_id, db=db)
    return templates.TemplateResponse("users/edit_user.html", {"request": request, "user": user})


@router.post("/user/update/{user_id}", response_class=RedirectResponse)
async def update_user(user_id: int, request: Request, db: Session = Depends(get_db), name: str = Form(...), email: str = Form(...)):
    await user_routes.update_user(request, user_id, schemas.UserBase(name=name, email=email), db=db)
    return RedirectResponse(url="/user", status_code=303)
