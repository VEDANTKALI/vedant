import os
import tempfile
import logging
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

logger = logging.getLogger("aivoa_qms.db")

Base = declarative_base()


def get_engine():
    """
    Attempts to connect to primary PostgreSQL DATABASE_URL.
    If PostgreSQL is unreachable or fails to connect, gracefully falls back to SQLite.
    Supports Vercel serverless /tmp path and in-memory fallback.
    """
    db_url = settings.DATABASE_URL
    try:
        if db_url and "postgresql" in db_url:
            engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20
            )
            # Test connection
            with engine.connect() as conn:
                logger.info("Connected successfully to primary PostgreSQL database.")
            return engine
    except Exception as e:
        logger.warning(f"Could not connect to PostgreSQL ({e}). Falling back to SQLite database.")

    # Determine SQLite URL
    is_serverless = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))
    if is_serverless:
        # Use /tmp with 4 slashes for absolute path on Linux
        sqlite_url = "sqlite:////tmp/aivoa_qms.db"
    else:
        sqlite_url = settings.SQLITE_FALLBACK_URL

    try:
        engine = create_engine(
            sqlite_url,
            connect_args={"check_same_thread": False}
        )
        # Test connection
        with engine.connect() as conn:
            pass
        logger.info(f"Using SQLite database engine: {sqlite_url}")
        return engine
    except Exception as e:
        logger.warning(f"File SQLite failed ({e}). Utilizing in-memory SQLite database.")
        return create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that yields a database session and closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
