from datetime import datetime
from pydantic import BaseModel
from models import Status


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: Status = Status.Pending
    created_at: datetime
    due_date: datetime


class CreateTask(TaskBase):
    project_id: int


class Task(TaskBase):
    id: int
    owner_id: int | None = None
    project_id: int


class UserBase(BaseModel):
    name: str
    email: str


class User(UserBase):
    id: int
    is_active: bool
    tasks: list[Task] = []


class ProjectBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime | None = None


class Project(ProjectBase):
    id: int
