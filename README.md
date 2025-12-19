# EdutrackAI - Integración WhatsApp

Servicio HTTP ligero que envía recordatorios de asistencia diaria a través de una API de WhatsApp configurable.

## Configuración

Configura las variables de entorno antes de iniciar el servidor:

- `WHATSAPP_API_URL` (requerido): endpoint de envío del proveedor de WhatsApp.
- `WHATSAPP_TOKEN` (requerido): token o clave de autenticación.
- `WHATSAPP_FROM` (opcional): identificador/remitente asignado por el proveedor.
- `WHATSAPP_TEMPLATE` (opcional): plantilla del mensaje. Usa `{{name}}` y `{{date}}` como marcadores.
- `PORT` (opcional): puerto del servidor HTTP. Por defecto 3000.

Ejemplo rápido con variables temporales:

```bash
WHATSAPP_API_URL=https://api.whatsapp.test/messages \
WHATSAPP_TOKEN=secreto \
node src/server.js
```

## Uso

### POST `/api/whatsapp/send`

Envía un mensaje de asistencia.

- Cuerpo JSON requerido: `{ "to": "<numero>", "studentName": "Ana", "date": "2025-01-01" }`
- Respuesta exitosa: preview del mensaje y respuesta del proveedor.

Ejemplo:

```bash
curl -X POST http://localhost:3000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{"to":"5215512345678","studentName":"Ana","date":"2025-01-01"}'
```

## Plantilla predeterminada

```
Asistencia diaria {{date}}: Hola {{name}}, confirma tu presencia respondiendo a este mensaje.
```

Los placeholders se reemplazan automáticamente; si faltan valores se usarán `estudiante` y la fecha local actual.
