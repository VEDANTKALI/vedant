import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

logger = logging.getLogger("aivoa_qms.db")

Base = declarative_base()


def get_engine():
    """
    Attempts to connect to primary PostgreSQL DATABASE_URL.
    If PostgreSQL is unreachable or fails to connect, gracefully falls back to SQLite.
    """
    db_url = settings.DATABASE_URL
    try:
        if "postgresql" in db_url:
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
    
    # SQLite Fallback
    sqlite_url = settings.SQLITE_FALLBACK_URL
    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False}
    )
    logger.info(f"Using SQLite database engine: {sqlite_url}")
    return engine


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
