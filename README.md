# EduTrack AI

API mínima para gestionar incidencias académicas.

## Endpoints
- **POST** `/api/incidents`: crea una incidencia registrando estudiante, docente que reporta, fecha, categoría, descripción y severidad.
- **GET** `/api/incidents?student_id=`: lista incidencias, opcionalmente filtradas por estudiante.
- **GET** `/api/incidents/{incident_id}`: consulta una incidencia específica.

## Puesta en marcha
1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

Los datos se mantienen en memoria para fines de demostración.
