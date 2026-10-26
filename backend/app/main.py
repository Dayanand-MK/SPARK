from fastapi import FastAPI
from app.api.routes.papers import router as papers_router
from app.config import settings
from sqlalchemy import text
from app.database import engine

# web app created
app = FastAPI(
    title = settings.app_name,
    description = "Scientific Paper Analysis & Research Knowledge Discovery",
    version = settings.app_version,
)

# HTTP GET endpoint
@app.get("/")
def root():
    return {
        "project" : "SPARK",
        "message" : "Scientific Paper Analysis API is running",
        "version" : "0.1.0",
    }

@app.get("/health")
def health():
    return {
        "status" : "healthy"
    }

@app.get("/config")
def config():
    return {
        "app_name" : settings.app_name,
        "environment" : settings.environment,
        "qdrant_collection" : settings.qdrant_collection,
    }

@app.get("/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database" : "PostgreSQL",
            "status" : "connected"
        }
    except Exception as exc:
        return {
            "database" : "PostgreSQL",
            "status" : "error",
            "detail" : str(exc)
        }

app.include_router(
    papers_router,
    prefix = "/papers",
    tags = ["Papers"]
)

