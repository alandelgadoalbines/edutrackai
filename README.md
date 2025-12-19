# EduTrack API

API mínima protegida con JWT para gestionar grados/secciones (classrooms) y estudiantes.

## Requisitos
- Node.js 18+
- Variable de entorno `JWT_SECRET` para firmar tokens.

## Instalación
```bash
npm install
```

> Si tu entorno no tiene acceso a internet, puedes instalar dependencias usando un mirror o empaquetar los módulos previamente.

## Ejecución
```bash
npm start
```
El servidor se levanta en `http://localhost:3000` por defecto.

## Autenticación
Genera un token de prueba:
```bash
curl -X POST http://localhost:3000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin"}'
```
Usa el token en los endpoints protegidos con `Authorization: Bearer <token>`.

## Endpoints
### Classrooms
- `GET /api/classrooms` lista todos los grados y secciones.
- `POST /api/classrooms` crea un classroom. Campos: `grade` (entero >=1), `section` (string requerido).

### Students
- `GET /api/students` lista estudiantes.
- `POST /api/students` crea un estudiante. Campos: `firstName`, `lastName`, `email`, `classroomId` existente.
- `PUT /api/students/:id` actualiza campos opcionales (`firstName`, `lastName`, `email`, `classroomId`).
- `DELETE /api/students/:id` elimina un estudiante.

## Validaciones
Los datos de entrada se validan con `express-validator`. Las respuestas de error incluyen un arreglo `errors` con los campos inválidos o un mensaje descriptivo.
