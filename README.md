# EduTrackAI API

Pequeña API con FastAPI que incorpora conexión reutilizable a MySQL usando SQLAlchemy.

## Configuración
1. Copia el archivo `.env.example` a `.env` y completa los valores:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASS`
   - `DB_NAME`
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```

## Salud de la base de datos
El endpoint `GET /api/health` intenta abrir una conexión a la base de datos y responde:
- `{ "status": "ok" }` cuando la conexión funciona.
- `{ "status": "error", "detail": "..." }` cuando hay problemas de configuración o conexión (sin exponer credenciales).
