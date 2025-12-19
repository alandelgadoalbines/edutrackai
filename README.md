# edutrackai

API básica de asistencia construida con FastAPI.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `POST /api/attendance` registra un movimiento de entrada o salida para un estudiante, usuario o acudiente. El registro se marca con la fecha y hora actual y la fuente `manual`.
- `GET /api/attendance?date=YYYY-MM-DD` devuelve los registros de asistencia del día solicitado ordenados cronológicamente.
