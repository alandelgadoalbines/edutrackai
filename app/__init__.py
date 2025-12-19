import os
from pathlib import Path

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()


def create_app() -> Flask:
    """Create and configure the Flask application."""

    # Cargar .env desde la raíz del proyecto (si existe)
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()

    app = Flask(__name__)

    # Config básica
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:////tmp/edutrackai.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar DB
    db.init_app(app)

    # Health endpoint (para probar en cPanel y local)
    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"})

    return app
