import app.models

from app.db.database import SessionLocal
from app.models.webhook_event import WebhookEvent


def process_webhook_event(webhook_event_id: int):
    
    db = SessionLocal()

    try:
        webhook_event = (
            db.query(WebhookEvent)
            .filter(WebhookEvent.id == webhook_event_id)
            .first()
        )

        if not webhook_event:
            print(
                f"Webhook event {webhook_event_id} not found"
            )
            return

        print(
            f"Processing webhook event "
            f"{webhook_event.id}: {webhook_event.event_type}"
        )

        # Real GitHub/PR processing will be added later.

        webhook_event.status = "processed"

        db.commit()

        print(
            f"Webhook event {webhook_event.id} processed successfully"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()