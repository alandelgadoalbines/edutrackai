# EduTrackAI - Reconocimiento facial en hosting compartido

Este servicio expone un API HTTP ligero para enrolar y verificar rostros sin almacenar fotografías. Solo se guardan los vectores de embeddings en un archivo JSON para maximizar la compatibilidad con hosting compartido (sin requerir GPU ni bases de datos).

## Requisitos

- Python 3.11+
- Dependencias en `requirements.txt`

## Puesta en marcha

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API

### POST `/api/face/enroll`
- **Body**
  - `user_id` (string): identificador único del usuario.
  - `image_base64` (string): imagen JPG/PNG codificada en base64.
  - `metadata` (object, opcional): información adicional (ej. cámara, sede).
- **Respuesta**
  - `user_id`: usuario enrolado.
  - `embedding_dim`: tamaño del vector almacenado.

### POST `/api/face/verify`
- **Body**
  - `image_base64` (string): imagen a validar.
  - `user_id` (string, opcional): restringe la comparación a un usuario concreto.
  - `tolerance` (float, opcional, default `0.5`): umbral de similitud (más bajo = más estricto).
- **Respuesta**
  - `matched` (bool): indica si la distancia es menor o igual al umbral.
  - `matched_user_id` (string | null): usuario coincidente cuando `matched` es verdadero.
  - `distance` (float | null): distancia mínima encontrada.

> El sistema nunca persiste imágenes; únicamente se guardan los embeddings en `app/data/embeddings.json`.

## Consideraciones para hosting compartido

- El almacenamiento usa un archivo JSON plano, evitando bases de datos.
- Las dependencias son 100% CPU (no requiere GPU). Si el host limita bibliotecas nativas, puedes generar los embeddings en un entorno controlado y cargar solo los vectores preprocesados.
- Para despliegues WSGI/ASGI (ej. cPanel con Passenger), apunta la app a `app.main:app`.

## Alternativa kiosko local (PC o Raspberry Pi)

Para escenarios offline o con hardware dedicado (p. ej., un kiosko de registro):
1. Ejecuta el mismo servicio en la máquina local usando `uvicorn`.
2. Conecta una cámara USB y captura imágenes desde el cliente (navegador o script Python) enviándolas en base64 a los endpoints anteriores.
3. Si la Raspberry Pi no puede compilar `dlib`/`face_recognition`, genera los embeddings en un equipo más potente y sincroniza el archivo `app/data/embeddings.json` al kiosko.
4. Configura un servicio systemd o un contenedor ligero para iniciar automáticamente el API al arrancar el dispositivo.

## Salud del servicio

- `GET /health` devuelve `{ "status": "ok" }` para checks de liveness.
