from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.analysis import Analysis
from app.models.pull_request import PullRequest
from app.workers.review_worker import analyze_pull_request


router = APIRouter(
    prefix="/pull-requests",
    tags=["Pull Requests"],
)


@router.get("")
def list_pull_requests(
    db: Session = Depends(get_db),
):
    pull_requests = (
        db.query(PullRequest)
        .order_by(PullRequest.created_at.desc())
        .all()
    )

    return pull_requests


@router.get("/{pull_request_id}")
def get_pull_request(
    pull_request_id: int,
    db: Session = Depends(get_db),
):
    pull_request = (
        db.query(PullRequest)
        .filter(PullRequest.id == pull_request_id)
        .first()
    )

    if not pull_request:
        raise HTTPException(
            status_code=404,
            detail="Pull request not found",
        )

    analysis = (
        db.query(Analysis)
        .filter(
            Analysis.pull_request_id == pull_request.id
        )
        .first()
    )

    return {
        "pull_request": pull_request,
        "analysis": analysis,
    }


@router.post("/{pull_request_id}/analyze")
def analyze_pull_request_route(
    pull_request_id: int,
    db: Session = Depends(get_db),
):
    pull_request = (
        db.query(PullRequest)
        .filter(PullRequest.id == pull_request_id)
        .first()
    )

    if not pull_request:
        raise HTTPException(
            status_code=404,
            detail="Pull request not found",
        )

    result = analyze_pull_request(pull_request_id)

    return {
        "message": "Pull request analysis completed",
        "pull_request_id": pull_request_id,
        "analysis_id": result["analysis_id"],
        "status": result["status"],
        "risk_score": result["risk_score"],
    }
