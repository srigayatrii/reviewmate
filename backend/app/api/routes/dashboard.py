from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.repository import Repository
from app.models.pull_request import PullRequest
from app.models.analysis import Analysis


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
):
    total_repositories = db.query(Repository).count()

    total_pull_requests = db.query(PullRequest).count()

    total_analyses = db.query(Analysis).count()

    open_pull_requests = (
        db.query(PullRequest)
        .filter(PullRequest.state == "open")
        .count()
    )

    completed_analyses = (
        db.query(Analysis)
        .filter(Analysis.status == "completed")
        .count()
    )

    high_risk = (
        db.query(Analysis)
        .filter(Analysis.risk_score == "high")
        .count()
    )

    medium_risk = (
        db.query(Analysis)
        .filter(Analysis.risk_score == "medium")
        .count()
    )

    low_risk = (
        db.query(Analysis)
        .filter(Analysis.risk_score == "low")
        .count()
    )

    recent_pull_requests = (
        db.query(PullRequest)
        .order_by(PullRequest.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "repositories": total_repositories,
        "pull_requests": total_pull_requests,
        "analyses": total_analyses,
        "open_pull_requests": open_pull_requests,
        "completed_analyses": completed_analyses,
        "risk_distribution": {
            "high": high_risk,
            "medium": medium_risk,
            "low": low_risk,
        },
        "recent_pull_requests": [
            {
                "id": pr.id,
                "title": pr.title,
                "pr_number": pr.pr_number,
                "state": pr.state,
                "author": pr.author,
                "created_at": pr.created_at,
                "repository_id": pr.repository_id,
            }
            for pr in recent_pull_requests
        ],
    }
