from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Analysis(BaseModel):
    __tablename__ = "analyses"

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    risk_score: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    missing_tests: Mapped[bool] = mapped_column(
        default=False
    )

    description_mismatch: Mapped[bool] = mapped_column(
        default=False
    )

    recommendations: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey("pull_requests.id"),
        unique=True
    )

    pull_request = relationship(
        "PullRequest",
        back_populates="analysis"
    )

    feedbacks = relationship(
        "Feedback",
        back_populates="analysis"
    )