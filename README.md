# EduTrack AI

API ligera para generar recomendaciones pedagógicas no punitivas a partir de incidencias y asistencia.

## Ejecución local

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicia el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Endpoint

`POST /api/ai/recommendations`

Ejemplo de payload:
```json
{
  "student": {"id": "123", "name": "Ana"},
  "attendance": {"total_sessions": 40, "absences": 5, "tardies": 3},
  "incidents": [
    {"type": "conducta", "severity": 4, "description": "Interrupciones"},
    {"type": "participación", "severity": 2}
  ]
}
```

Respuesta esperada:
```json
{
  "student": {"id": "123", "name": "Ana"},
  "recommendations": [
    {"category": "asistencia", "message": "Coordinar con la familia...", "priority": 1},
    {"category": "puntualidad", "message": "Proponer rutinas de llegada...", "priority": 2},
    {"category": "conducta", "message": "Realizar una conversación individual breve...", "priority": 1},
    {"category": "participación", "message": "Planificar intervenciones cortas...", "priority": 2}
  ],
  "summary": "Plan sugerido para Ana con foco en: conducta, asistencia, puntualidad, participación."
}
```

Las recomendaciones son breves y orientadas a tutoría, sin tono punitivo.
