from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class WebhookEvent(BaseModel):
    __tablename__ = "webhook_events"

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id")
    )

    repository = relationship(
        "Repository",
        back_populates="webhook_events"
    )