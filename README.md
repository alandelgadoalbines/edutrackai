# EduTrackAI API

API HTTP mínima con autenticación JWT, hashing seguro de contraseñas y roles (`admin`, `docente`, `administrativo`). Incluye un usuario administrador inicial y middleware para proteger rutas.

## Configuración

1. Copia `.env.example` a `.env` y ajusta valores:
   - `JWT_SECRET`: clave larga y secreta para firmar los tokens.
   - `ADMIN_PASSWORD`: contraseña del usuario admin inicial.
   - `PORT` y `JWT_EXPIRES_IN` opcionales.
2. Instala Node.js (v18+).
3. Ejecuta el servidor:

```bash
npm start
```

El servidor escucha en `http://localhost:3000` (o el puerto configurado).

## Usuario inicial

- **Email:** `admin@example.com`
- **Password:** `Admin123!` (o el valor que definas en `ADMIN_PASSWORD`)
- **Rol:** `admin`

Las contraseñas se almacenan con `scrypt` + salt aleatoria.

## Endpoints

### POST `/api/auth/login`
Solicita credenciales y retorna un JWT.

Cuerpo ejemplo:
```json
{
  "email": "admin@example.com",
  "password": "Admin123!"
}
```

Respuesta exitosa:
```json
{
  "token": "<jwt>",
  "expiresIn": 3600,
  "user": {
    "id": "1",
    "email": "admin@example.com",
    "role": "admin",
    "displayName": "Administrador Inicial"
  }
}
```

### GET `/api/auth/me`
Requiere header `Authorization: Bearer <token>`. Devuelve los datos del usuario autenticado.

### GET `/api/admin/example`
Ejemplo de ruta protegida solo para rol `admin`. Requiere token válido con rol adecuado.

### GET `/api/auth/roles`
Devuelve los roles soportados (`admin`, `docente`, `administrativo`).

## Middleware

Usa `Authorization: Bearer <token>` para validar tokens y opcionalmente restringir por roles. Si el token es inválido o el rol no está autorizado, responde con `401/403`.
