from __future__ import annotations

import base64
import io
from typing import Dict, List, Optional, Tuple

import face_recognition
import numpy as np
from pydantic import BaseModel, Field

from .storage import EmbeddingStore, StoredEmbedding


class EnrollRequest(BaseModel):
    user_id: str = Field(..., description="Identificador del usuario a enrolar")
    image_base64: str = Field(..., description="Imagen en base64 (JPG/PNG)")
    metadata: Optional[Dict[str, str]] = Field(
        default=None, description="Información adicional (ej. sucursal, cámara)"
    )


class EnrollResponse(BaseModel):
    user_id: str
    embedding_dim: int


class VerifyRequest(BaseModel):
    image_base64: str
    user_id: Optional[str] = Field(
        default=None,
        description="Si se envía, solo se compara contra las muestras de ese usuario",
    )
    tolerance: float = Field(
        default=0.5,
        description="Umbral de distancia facial. Valores más bajos son más estrictos",
    )


class VerifyResponse(BaseModel):
    matched: bool
    matched_user_id: Optional[str]
    distance: Optional[float]


class FaceService:
    def __init__(self, store: EmbeddingStore):
        self.store = store

    def _decode_image(self, b64: str) -> np.ndarray:
        try:
            image_data = base64.b64decode(b64)
            stream = io.BytesIO(image_data)
            return face_recognition.load_image_file(stream)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("No se pudo decodificar la imagen") from exc

    def _extract_embedding(self, image: np.ndarray) -> np.ndarray:
        locations = face_recognition.face_locations(image)
        if not locations:
            raise ValueError("No se detectaron rostros en la imagen")
        embeddings = face_recognition.face_encodings(image, known_face_locations=locations)
        if not embeddings:
            raise ValueError("No se pudo generar el embedding facial")
        return embeddings[0]

    def enroll(self, payload: EnrollRequest) -> EnrollResponse:
        image = self._decode_image(payload.image_base64)
        embedding = self._extract_embedding(image)
        record = StoredEmbedding(
            user_id=payload.user_id,
            embedding=embedding.tolist(),
            metadata=payload.metadata,
        )
        self.store.add(record)
        return EnrollResponse(user_id=payload.user_id, embedding_dim=len(record.embedding))

    def verify(self, payload: VerifyRequest) -> VerifyResponse:
        image = self._decode_image(payload.image_base64)
        probe = self._extract_embedding(image)
        candidates = self.store.embeddings_for(payload.user_id)
        if not candidates:
            return VerifyResponse(matched=False, matched_user_id=None, distance=None)

        best_user: Optional[str] = None
        best_distance: Optional[float] = None

        for user_id, entries in candidates.items():
            stored_vectors = np.array([entry.embedding for entry in entries])
            distances = face_recognition.face_distance(stored_vectors, probe)
            user_best = float(np.min(distances))
            if best_distance is None or user_best < best_distance:
                best_distance = user_best
                best_user = user_id

        matched = best_distance is not None and best_distance <= payload.tolerance
        return VerifyResponse(
            matched=matched, matched_user_id=best_user if matched else None, distance=best_distance
        )
