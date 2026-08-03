from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class PullRequest(BaseModel):
    __tablename__ = "pull_requests"

    github_pr_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False
    )

    pr_number: Mapped[int] = mapped_column(
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    state: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    base_branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    head_branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"),
        nullable=False
    )

    repository = relationship(
        "Repository",
        back_populates="pull_requests"
    )

    analysis = relationship(
        "Analysis",
        back_populates="pull_request",
        uselist=False
    )
    files = relationship(
        "PullRequestFile",
        back_populates="pull_request",
        cascade="all, delete-orphan"
    )