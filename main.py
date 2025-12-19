from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="EduTrack AI API")


class IncidentCreate(BaseModel):
    student_id: str = Field(..., description="Identificador del estudiante")
    teacher_id: str = Field(..., description="Docente que reporta")
    date: datetime = Field(..., description="Fecha en que ocurrió la incidencia")
    category: str = Field(..., description="Categoría de la incidencia")
    description: str = Field(..., description="Descripción detallada")
    severity: str = Field(..., description="Nivel de severidad")


class Incident(IncidentCreate):
    id: int


_incidents: List[Incident] = []


def _next_id() -> int:
    return len(_incidents) + 1


@app.post("/api/incidents", response_model=Incident, status_code=201)
def create_incident(incident: IncidentCreate) -> Incident:
    new_incident = Incident(id=_next_id(), **incident.model_dump())
    _incidents.append(new_incident)
    return new_incident


@app.get("/api/incidents", response_model=List[Incident])
def list_incidents(student_id: Optional[str] = Query(None, description="Filtrar por estudiante")) -> List[Incident]:
    if student_id:
        return [incident for incident in _incidents if incident.student_id == student_id]
    return list(_incidents)


@app.get("/api/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: int) -> Incident:
    try:
        return _incidents[incident_id - 1]
    except IndexError as exc:  # pragma: no cover - errores de búsqueda
        raise HTTPException(status_code=404, detail="Incidencia no encontrada") from exc
