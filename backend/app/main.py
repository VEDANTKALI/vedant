import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import engine
from app.db.base import Base
from app.db.seed import seed_database
from app.api.routes import complaints, dashboard, health

setup_logging()
logger = logging.getLogger("aivoa_qms.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Aivoa QMS Backend Application...")
    # Initialize DB tables
    try:
        Base.metadata.create_all(bind=engine)
        seed_database()
    except Exception as e:
        logger.error(f"Error during DB initialization: {e}")
    yield
    logger.info("Shutting down Aivoa QMS Backend Application.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(complaints.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Welcome to Aivoa.ai AI-Powered Customer Complaint Management System API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
