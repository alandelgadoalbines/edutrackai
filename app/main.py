from __future__ import annotations

from datetime import date, datetime, time
from typing import List

from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from . import models
from .database import Base, SessionLocal, engine
from .schemas import AttendanceCreate, AttendanceListResponse, AttendanceRead

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/attendance", response_model=AttendanceRead, status_code=201)
def create_attendance(entry: AttendanceCreate, db: Session = Depends(get_db)):
    timestamp = datetime.utcnow()
    attendance = models.Attendance(
        person_type=entry.person_type,
        direction=entry.direction,
        timestamp=timestamp,
        source="manual",
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


@app.get("/api/attendance", response_model=AttendanceListResponse)
def list_attendance(
    date_filter: date = Query(..., description="Fecha a consultar en formato YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    start_of_day = datetime.combine(date_filter, time.min)
    end_of_day = datetime.combine(date_filter, time.max)

    records: List[models.Attendance] = (
        db.query(models.Attendance)
        .filter(models.Attendance.timestamp >= start_of_day)
        .filter(models.Attendance.timestamp <= end_of_day)
        .order_by(models.Attendance.timestamp.asc())
        .all()
    )

    return AttendanceListResponse(date=date_filter, records=records)
