# EduTrackAI Dashboard

Frontend liviano para el consumo de la API `https://adahost.pe/edutrackai/api`.

## Características
- Inicio de sesión con almacenamiento del JWT en `localStorage`.
- Visualización de asistencia con actualización manual.
- Registro de incidencias.
- Descarga de Excel desde el endpoint de exportación de asistencia.

## Uso
1. Sirve los archivos estáticos (por ejemplo, con `npx serve .` o cualquier servidor web).
2. Ingresa tus credenciales y presiona **Acceder**. El JWT se guarda en `localStorage`.
3. Usa **Actualizar** para obtener asistencia, **Descargar Excel** para el archivo y completa el formulario para registrar incidencias.

### Endpoints esperados
Los endpoints configurados en `script.js` son:
- `POST /login` → devuelve `{ token: "jwt" }`.
- `GET /attendance` → devuelve un arreglo de registros.
- `POST /incidents` → crea una incidencia.
- `GET /attendance/export` → descarga un archivo Excel.

Ajusta las rutas o el manejo de respuestas según la implementación real de la API si fuera necesario.
