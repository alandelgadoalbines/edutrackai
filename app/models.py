from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SqlEnum, Integer, String

from .database import Base


class PersonType(str, Enum):
    STUDENT = "student"
    USER = "user"
    GUARDIAN = "guardian"


class AttendanceDirection(str, Enum):
    IN = "IN"
    OUT = "OUT"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    person_type = Column(SqlEnum(PersonType), nullable=False, index=True)
    direction = Column(SqlEnum(AttendanceDirection), nullable=False)
    timestamp = Column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
    source = Column(String, default="manual", nullable=False)
