from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    github_id: Mapped[int] = mapped_column(
        unique=True,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    avatar_url: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    access_token: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    repositories = relationship(
        "Repository",
        back_populates="owner"
    )

    feedbacks = relationship(
        "Feedback",
        back_populates="user"
    )