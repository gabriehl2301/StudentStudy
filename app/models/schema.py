from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sqla
import sqlalchemy.orm as orm
from app import db
from flask_login import UserMixin
from enum import StrEnum, auto

class TaskStatus(StrEnum):
    Active = auto()
    Cancelled = auto()
    Complete = auto()

class User(UserMixin, db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    email: orm.Mapped[str] = orm.mapped_column(sqla.String(255), index=True, unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sqla.String(255))

class Task(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sqla.ForeignKey("user.id"), nullable=False)
    task_name: orm.Mapped[str] = orm.mapped_column(sqla.String(200), nullable=False)
    status: orm.Mapped[TaskStatus] = orm.mapped_column(sqla.Enum(TaskStatus), default=TaskStatus.Active)
    created_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.now(timezone.utc))

    user: orm.Mapped["User"] = orm.relationship(back_populates="tasks")

# Add a relationship to the User model
User.tasks = orm.relationship("Task", back_populates="user")