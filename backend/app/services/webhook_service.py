from rq import Retry
from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.webhook_event import WebhookEvent
from app.workers.redis_queue import queue
from app.workers.tasks import process_webhook_event


class WebhookService:

    def __init__(self, db: Session):
        self.db = db

    def process_event(
        self,
        event_type: str,
        payload: dict
    ):

        repository = (
            self.db.query(Repository)
            .filter(
                Repository.full_name
                == payload["repository"]["full_name"]
            )
            .first()
        )

        webhook_event = WebhookEvent(
            event_type=event_type,
            payload=payload,
            repository_id=repository.id,
        )

        # Store webhook event in PostgreSQL
        self.db.add(webhook_event)
        self.db.commit()
        self.db.refresh(webhook_event)

        # Send background job to Redis
        queue.enqueue(
            process_webhook_event,
            webhook_event.id,
            retry=Retry(
                max=3,
                interval=[10, 30, 60]
            )
        )

        # Dispatch based on GitHub event type
        if event_type == "push":
            self.handle_push(webhook_event)

        elif event_type == "pull_request":
            self.handle_pull_request(webhook_event)

        elif event_type == "ping":
            self.handle_ping(webhook_event)

        return webhook_event

    def handle_push(
        self,
        webhook_event: WebhookEvent
    ):
        print("Processing push event")

    def handle_pull_request(
        self,
        webhook_event: WebhookEvent
    ):
        print("Processing pull request event")

    def handle_ping(
        self,
        webhook_event: WebhookEvent
    ):
        print("Processing ping event")