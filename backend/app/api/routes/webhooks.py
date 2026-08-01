from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.security import verify_github_signature
from app.db.dependencies import get_db
from app.models.repository import Repository
from app.models.webhook_event import WebhookEvent
from app.services.webhook_service import WebhookService

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


@router.post("/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(...),
    db: Session = Depends(get_db)
):

    payload = await request.body()

    if not verify_github_signature(
        payload,
        x_hub_signature_256
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook signature"
        )

    data = await request.json()

    event_type = request.headers.get("X-GitHub-Event")

    service = WebhookService(db)

    webhook_event = service.process_event(
        event_type=event_type,
        payload=data
    )

    return {
        "message": "Webhook stored successfully",
        "event_id": webhook_event.id,
        "event_type": event_type
    }