from typing import Optional 
from datetime import datetime, timezone, time as paytime, date as pydate
import sqlalchemy as sqla
import sqlalchemy.orm as orm 
from app import db 
from flask_login import UserMixin 
from enum import StrEnum, auto 


class TaskStatus(StrEnum):
    Active=auto()
    Cancelled = auto()
    Complete = auto()

class User( UserMixin, db.Model):
    id: orm.Mapped[int] = orm.mapped_column( primary_key = True, autoincrement = True)
    email: orm.Mapped[str] = orm.mapped_column(sqla.String(255), index = True, unique=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sqla.String(255))