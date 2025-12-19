from __future__ import annotations

from datetime import datetime, date
from typing import List
from pydantic import BaseModel, Field

from .models import AttendanceDirection, PersonType


class AttendanceBase(BaseModel):
    person_type: PersonType = Field(..., description="Tipo de persona")
    direction: AttendanceDirection = Field(..., description="Dirección de asistencia (IN/OUT)")


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    id: int
    timestamp: datetime
    source: str

    class Config:
        orm_mode = True


class AttendanceListResponse(BaseModel):
    date: date
    records: List[AttendanceRead]
