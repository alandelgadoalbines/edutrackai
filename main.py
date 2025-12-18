from fastapi import FastAPI

from database import check_connection

app = FastAPI(title="EduTrackAI API")


@app.get("/api/health")
async def health_check():
    connected, message = check_connection()

    if connected:
        return {"status": "ok"}

    return {
        "status": "error",
        "detail": message or "Database connection unavailable.",
    }
