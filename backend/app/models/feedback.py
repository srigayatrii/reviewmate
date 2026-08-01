from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Feedback(BaseModel):
    __tablename__ = "feedback"

    is_helpful: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    comment: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    analysis_id: Mapped[int] = mapped_column(
        ForeignKey("analyses.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    analysis = relationship(
        "Analysis",
        back_populates="feedbacks"
    )

    user = relationship(
        "User",
        back_populates="feedbacks"
    )