import os
import logging
from typing import Generator, Tuple

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

load_dotenv()

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


class DatabaseConfigError(Exception):
    """Raised when the database configuration is incomplete."""


def _require_env() -> Tuple[str, str, str, str]:
    missing = [name for name, value in {
        "DB_HOST": DB_HOST,
        "DB_USER": DB_USER,
        "DB_PASS": DB_PASS,
        "DB_NAME": DB_NAME,
    }.items() if not value]

    if missing:
        raise DatabaseConfigError(
            f"Missing required database environment variables: {', '.join(missing)}"
        )

    return DB_HOST, DB_USER, DB_PASS, DB_NAME


def _build_database_url() -> str:
    host, user, password, name = _require_env()
    return f"mysql+pymysql://{user}:{password}@{host}/{name}"


try:
    DATABASE_URL = _build_database_url()
except DatabaseConfigError:
    DATABASE_URL = ""

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    future=True,
) if DATABASE_URL else None

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) if engine else None


def get_db() -> Generator:
    """Provide a transactional scope around a series of operations."""
    if SessionLocal is None:
        raise DatabaseConfigError("Database session is not configured. Check environment variables.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> Tuple[bool, str]:
    """Attempt to connect to the database returning success and a sanitized message."""
    if engine is None:
        return False, "Database is not configured."

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, ""
    except SQLAlchemyError as exc:
        logger.warning("Database connection attempt failed: %s", exc)
        return False, "Database connection failed."
