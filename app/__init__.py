from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify


def create_app() -> Flask:
    """Application factory for the EduTrackAI backend."""
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()

    app = Flask(__name__)

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"})

    return app
