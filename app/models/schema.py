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
    Not_Started = auto()

class User(UserMixin, db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    email: orm.Mapped[str] = orm.mapped_column(sqla.String(255), index=True, unique=True)
    name: orm.Mapped[str] = orm.mapped_column(sqla.String(255), index=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sqla.String(255) )

class Task(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sqla.ForeignKey("user.id"), nullable=False)
    task_name: orm.Mapped[str] = orm.mapped_column(sqla.String(200), nullable=False)
    status: orm.Mapped[TaskStatus] = orm.mapped_column(sqla.Enum(TaskStatus), default=TaskStatus.Active)
    category: orm.Mapped[str] = orm.mapped_column(sqla.String(50), nullable=False) 
    created_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.now(timezone.utc))
    start_date: orm.Mapped[Optional[datetime.date]] = orm.mapped_column(sqla.Date)
    end_date: orm.Mapped[Optional[datetime.date]] = orm.mapped_column(sqla.Date)

    user: orm.Mapped["User"] = orm.relationship(back_populates="tasks")

# Add a relationship to the User model
User.tasks = orm.relationship("Task", back_populates="user")

class Log(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sqla.ForeignKey("user.id"), nullable=False)
    action: orm.Mapped[str] = orm.mapped_column(sqla.String(255), nullable=False)
    timestamp: orm.Mapped[datetime] = orm.mapped_column(default=datetime.now(timezone.utc))

    # Relationships
    user: orm.Mapped["User"] = orm.relationship(back_populates="logs")

# Add a relationship to the User model
User.logs = orm.relationship("Log", back_populates="user")

