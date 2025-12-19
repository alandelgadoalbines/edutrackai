from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel


class StoredEmbedding(BaseModel):
    user_id: str
    embedding: List[float]
    metadata: Optional[Dict[str, str]] = None


class EmbeddingStore:
    """Lightweight JSON store to keep facial embeddings without images."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._records: Dict[str, List[StoredEmbedding]] = {}
        if self.path.exists():
            self._load()

    def _load(self) -> None:
        raw = json.loads(self.path.read_text()) if self.path.read_text() else {}
        self._records = {
            user_id: [StoredEmbedding(**entry) for entry in entries]
            for user_id, entries in raw.items()
        }

    def _persist(self) -> None:
        serializable = {
            user_id: [record.model_dump() for record in entries]
            for user_id, entries in self._records.items()
        }
        self.path.write_text(json.dumps(serializable, indent=2))

    def add(self, record: StoredEmbedding) -> None:
        self._records.setdefault(record.user_id, []).append(record)
        self._persist()

    def embeddings_for(self, user_id: Optional[str] = None) -> Dict[str, List[StoredEmbedding]]:
        if user_id:
            if user_id not in self._records:
                return {}
            return {user_id: self._records[user_id]}
        return self._records
