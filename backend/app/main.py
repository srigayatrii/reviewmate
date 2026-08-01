from fastapi import FastAPI
from app.api.routes.worker import router as worker_router
from app.api.routes.auth import router as auth_router
from app.core.logging import logger
from app.api.routes.webhooks import router as webhook_router
from app.models.user import User
from app.models.repository import Repository
from app.models.pull_request import PullRequest
from app.models.analysis import Analysis
from app.models.feedback import Feedback
from app.models.webhook_event import WebhookEvent
from app.api.routes.repositories import router as repository_router

app = FastAPI(
    title="ReviewMate API",
    description="AI-Powered Code Review Platform",
    version="1.0.0"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    repository_router,
    prefix="/api/v1"
)

@app.on_event("startup")
def startup_event():
    logger.info("ReviewMate API started successfully")


@app.get("/")
def health_check():
    logger.info("Health check endpoint called")

    return {
        "message": "Welcome to ReviewMate API"
    }

app.include_router(
    webhook_router,
    prefix="/api/v1"
)

app.include_router(
    worker_router,
    prefix="/api/v1"
)