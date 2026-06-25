from fastapi import FastAPI

from app.core.config import settings
from app.db.database import check_database_connection
from app.routers import service_queues, tickets


app = FastAPI(
    title=settings.app_name,
    description="Digital queue management system for physical service businesses.",
    version="0.1.0",
)


app.include_router(service_queues.router)
app.include_router(tickets.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to QueueFlow API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@app.get("/health/db")
def database_health_check():
    check_database_connection()

    return {
        "database": "connected",
    }