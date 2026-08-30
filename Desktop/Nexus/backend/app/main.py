"""DevHub FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.config import settings
from app.database import Base, engine

logger = logging.getLogger("devhub")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Create tables and seed demo data on startup."""
    # Import models so metadata is populated before create_all.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    if settings.seed_demo:
        from app.seed import seed_demo_data

        seed_demo_data()
    logger.info("DevHub API started")
    yield


app = FastAPI(
    title=f"{settings.app_name} API",
    version="1.0.0",
    description="Backend API for DevHub — learning, jobs, marketplace and payments.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve locally-uploaded media (only used as a fallback; S3 is used in production).
Path("media").mkdir(exist_ok=True)
try:
    app.mount("/media", StaticFiles(directory="media"), name="media")
except RuntimeError:
    pass

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["health"])
def root():
    return {"name": settings.app_name, "status": "ok", "docs": "/docs"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
