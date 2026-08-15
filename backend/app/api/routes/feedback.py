from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.analysis import Analysis
from app.schemas.feedback import FeedbackCreate
from fastapi import HTTPException
from app.db.dependencies import get_db
from app.models.feedback import Feedback
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)

@router.post("")
def create_feedback(
    feedback: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == feedback.analysis_id)
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    new_feedback = Feedback(
        analysis_id=feedback.analysis_id,
        is_helpful=feedback.is_helpful,
        comment=feedback.comment,
        user_id=current_user.id,
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback