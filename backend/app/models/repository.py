from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Repository(BaseModel):
    __tablename__ = "repositories"

    github_repo_id: Mapped[int] = mapped_column(
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    owner_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="repositories"
    )

    pull_requests = relationship(
        "PullRequest",
        back_populates="repository"
    )

    webhook_events = relationship(
        "WebhookEvent",
        back_populates="repository"
    )