# EduTrack API

Servicio FastAPI sencillo para exportar reportes de asistencia en formato Excel.

## Ejecución local

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicia el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

## Exportar asistencia

```
GET /api/reports/attendance.xlsx?period=daily&grade=1&section=A
```

Parámetros admitidos:
- `period`: `daily` | `monthly` | `yearly`
- `grade`: filtro opcional de grado
- `section`: filtro opcional de sección

La respuesta descarga un archivo Excel con el resumen de asistencia agrupado según el periodo solicitado.
