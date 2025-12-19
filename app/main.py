from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .face_service import (
    EnrollRequest,
    EnrollResponse,
    FaceService,
    VerifyRequest,
    VerifyResponse,
)
from .storage import EmbeddingStore

app = FastAPI(title="EduTrackAI Face API", version="1.0.0")
store = EmbeddingStore(Path("app/data/embeddings.json"))
service = FaceService(store)


@app.post("/api/face/enroll", response_model=EnrollResponse)
def enroll(request: EnrollRequest) -> Any:
    try:
        return service.enroll(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/face/verify", response_model=VerifyResponse)
def verify(request: VerifyRequest) -> Any:
    try:
        return service.verify(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
