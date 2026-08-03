from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class PullRequestFile(BaseModel):
    __tablename__ = "pull_request_files"

    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    additions: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    deletions: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    changes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    patch: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey("pull_requests.id"),
        nullable=False
    )

    pull_request = relationship(
        "PullRequest",
        back_populates="files"
    )