from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    analysis_id: int
    is_helpful: bool
    comment: str | None = None