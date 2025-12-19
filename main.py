from collections import Counter
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, PositiveInt, conint, validator


class StudentProfile(BaseModel):
    id: Optional[str] = Field(None, description="Identificador único del estudiante")
    name: Optional[str] = Field(None, description="Nombre del estudiante")


class Incident(BaseModel):
    type: str = Field(..., description="Tipo de incidencia, por ejemplo 'conducta' o 'participación'")
    severity: conint(ge=1, le=5) = Field(
        ..., description="Grado de impacto de la incidencia en una escala de 1 a 5"
    )
    description: Optional[str] = Field(None, description="Detalles breves de la incidencia")
    date: Optional[str] = Field(
        None, description="Fecha ISO de la incidencia. Se valida a nivel de cliente"
    )


class Attendance(BaseModel):
    total_sessions: PositiveInt = Field(..., description="Número total de sesiones registradas")
    absences: conint(ge=0) = Field(0, description="Sesiones a las que no asistió")
    tardies: conint(ge=0) = Field(0, description="Llegadas tarde registradas")

    @validator("absences", "tardies")
    def non_negative(cls, value: int) -> int:
        return max(0, value)

    @validator("absences")
    def absences_not_exceed_total(cls, value: int, values) -> int:
        total = values.get("total_sessions")
        if total is not None and value > total:
            raise ValueError("Las ausencias no pueden superar las sesiones totales")
        return value


class RecommendationRequest(BaseModel):
    student: Optional[StudentProfile] = None
    incidents: List[Incident] = Field(default_factory=list)
    attendance: Optional[Attendance] = None


class Recommendation(BaseModel):
    category: str
    message: str
    priority: conint(ge=1, le=3) = Field(
        2, description="Prioridad pedagógica de 1 (alta) a 3 (baja)"
    )


class RecommendationResponse(BaseModel):
    student: Optional[StudentProfile]
    recommendations: List[Recommendation]
    summary: str


app = FastAPI(title="EduTrack AI", version="0.1.0")


def _attendance_insights(attendance: Attendance) -> List[Recommendation]:
    total = attendance.total_sessions
    absences = attendance.absences
    tardies = attendance.tardies
    attendance_rate = (total - absences) / total

    suggestions: List[Recommendation] = []

    if attendance_rate < 0.9:
        suggestions.append(
            Recommendation(
                category="asistencia",
                message=(
                    "Coordinar con la familia un plan ligero de seguimiento para mejorar la asistencia, "
                    "con recordatorios previos y flexibilidad en casos justificados."
                ),
                priority=1,
            )
        )

    if tardies / total > 0.1:
        suggestions.append(
            Recommendation(
                category="puntualidad",
                message=(
                    "Proponer rutinas de llegada y acordar con el estudiante objetivos semanales de puntualidad "
                    "con retroalimentación positiva."
                ),
                priority=2,
            )
        )

    if not suggestions:
        suggestions.append(
            Recommendation(
                category="asistencia",
                message="Mantener las estrategias actuales: la asistencia y puntualidad son consistentes.",
                priority=3,
            )
        )

    return suggestions


def _incident_insights(incidents: List[Incident]) -> List[Recommendation]:
    if not incidents:
        return [
            Recommendation(
                category="bienestar",
                message="Refuerza los logros recientes y acuerda nuevos retos breves para sostener la motivación.",
                priority=3,
            )
        ]

    counts = Counter(incident.type.lower() for incident in incidents)
    highest = counts.most_common(2)
    suggestions: List[Recommendation] = []

    for incident_type, _ in highest:
        if incident_type == "conducta":
            suggestions.append(
                Recommendation(
                    category="conducta",
                    message=(
                        "Realizar una conversación individual breve para definir apoyos y acuerdos de convivencia, "
                        "enfocada en identificar detonantes y alternativas."),
                    priority=1,
                )
            )
        elif incident_type == "participación":
            suggestions.append(
                Recommendation(
                    category="participación",
                    message=(
                        "Planificar intervenciones cortas con preguntas guiadas y reconocimiento inmediato "
                        "cuando comparta ideas."),
                    priority=2,
                )
            )
        else:
            suggestions.append(
                Recommendation(
                    category=incident_type,
                    message=(
                        "Registrar ejemplos concretos con el estudiante y co-diseñar estrategias prácticas "
                        "para la siguiente semana."),
                    priority=2,
                )
            )

    return suggestions


def _merge_recommendations(attendance: Optional[Attendance], incidents: List[Incident]) -> List[Recommendation]:
    recommendations: List[Recommendation] = []
    if attendance:
        recommendations.extend(_attendance_insights(attendance))
    recommendations.extend(_incident_insights(incidents))

    seen = set()
    unique: List[Recommendation] = []
    for rec in recommendations:
        key = (rec.category, rec.message)
        if key not in seen:
            seen.add(key)
            unique.append(rec)
    return unique[:5]


def _summary(student: Optional[StudentProfile], recommendations: List[Recommendation]) -> str:
    name = student.name if student and student.name else "el estudiante"
    focus = ", ".join({rec.category for rec in recommendations})
    return f"Plan sugerido para {name} con foco en: {focus}."


@app.post("/api/ai/recommendations", response_model=RecommendationResponse)
def generate_recommendations(payload: RecommendationRequest) -> RecommendationResponse:
    if payload.attendance is None and not payload.incidents:
        raise HTTPException(
            status_code=400, detail="Se requiere asistencia o incidencias para generar recomendaciones"
        )

    recommendations = _merge_recommendations(payload.attendance, payload.incidents)
    return RecommendationResponse(
        student=payload.student,
        recommendations=recommendations,
        summary=_summary(payload.student, recommendations),
    )


@app.get("/")
def root() -> dict:
    return {"status": "ok"}
