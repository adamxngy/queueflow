from fastapi import FastAPI

app = FastAPI(
    title="QueueFlow API",
    description="Digital queue management system for physical service businesses.",
    version="0.1.0",
)


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
