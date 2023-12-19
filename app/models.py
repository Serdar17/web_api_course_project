from sqlalchemy import Table, Enum, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from enums import Status

from database import Base

user_group_associations = Table(
    'user_group_associations',
    Base.metadata,
    Column("user_id", Integer, ForeignKey('users.id'), nullable=True),
    Column("project_id", Integer, ForeignKey('projects.id'), nullable=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")
    projects = relationship('Project', secondary=user_group_associations, back_populates="users")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    users = relationship(
        "User",
        secondary=user_group_associations,
        back_populates="projects")
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade='all, delete-orphan')


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(Status), default=Status.Pending)
    created_at = Column(DateTime, nullable=False)
    due_date = Column(DateTime)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    owner = relationship("User", back_populates="tasks")

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    project = relationship("Project", back_populates="tasks")
