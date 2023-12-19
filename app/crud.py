from sqlalchemy.orm import Session
from models import User, Task, Project
from schemas import UserBase, ProjectBase, CreateTask


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserBase):
    db_user = User(email=user.email, name=user.name, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: UserBase, user_id: int):
    exist_user = get_user(db, user_id=user_id)
    if exist_user:
        exist_user.name = user.name
        exist_user.email = user.email
        db.commit()
    return exist_user


def delete_user(db: Session, user_id: int):
    exist_user = get_user(db, user_id=user_id)
    if exist_user:
        db.delete(exist_user)
        db.commit()
    return exist_user


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, project: ProjectBase):
    db_project = Project(
        title=project.title,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectBase):
    exist_project = get_project_by_id(db, project_id=project_id)
    if exist_project:
        exist_project.title = project.title
        exist_project.description = project.description
        exist_project.start_date = project.start_date
        exist_project.end_date = project.end_date
        db.commit()
    return exist_project


def delete_project(db: Session, project_id: int):
    exist_project = get_project_by_id(db, project_id=project_id)
    if exist_project:
        db.delete(exist_project)
        db.commit()
    return exist_project


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: CreateTask):
    db_task = Task(
        title=task.title,
        description=task.description,
        created_at=task.created_at,
        status=task.status,
        due_date=task.due_date,
        project_id=task.project_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: CreateTask):
    exist_task = get_task(db, task_id=task_id)
    if exist_task:
        exist_task.title = task.title
        exist_task.description = task.description
        exist_task.status = task.status
        exist_task.due_date = task.due_date
        exist_task.created_at = task.created_at
        exist_task.project_id = task.project_id
        db.commit()
        print(exist_task.project_id)
    return exist_task


def delete_task(db: Session, task_id: int):
    exist_task = get_task(db, task_id=task_id)
    if exist_task:
        db.delete(exist_task)
        db.commit()
    return exist_task
