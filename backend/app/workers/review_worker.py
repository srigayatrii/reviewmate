import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.analysis import Analysis
from app.models.pull_request import PullRequest
from app.models.repository import Repository
from app.models.user import User
from app.github.client import GitHubClient
from app.ai.client import AIClient


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def analyze_pull_request(pull_request_id: int):
    db = SessionLocal()

    try:
        # 1. Find PR
        pull_request = (
            db.query(PullRequest)
            .filter(PullRequest.id == pull_request_id)
            .first()
        )

        if not pull_request:
            raise ValueError(
                f"Pull request {pull_request_id} not found"
            )

        # 2. Find repository
        repository = (
            db.query(Repository)
            .filter(
                Repository.id == pull_request.repository_id
            )
            .first()
        )

        if not repository:
            raise ValueError(
                f"Repository {pull_request.repository_id} not found"
            )

        # 3. Find GitHub user/token
        user = (
            db.query(User)
            .filter(
                User.id == repository.user_id
            )
            .first()
        )

        if not user:
            raise ValueError(
                f"User {repository.user_id} not found"
            )

        # 4. Get existing analysis
        analysis = (
            db.query(Analysis)
            .filter(
                Analysis.pull_request_id == pull_request.id
            )
            .first()
        )

        if not analysis:
            analysis = Analysis(
                pull_request_id=pull_request.id,
                status="pending",
                risk_score="unknown",
                missing_tests=False,
                description_mismatch=False,
                summary="",
                recommendations="",
            )

            db.add(analysis)
            db.commit()
            db.refresh(analysis)

        analysis.status = "processing"
        db.commit()

        # 5. GitHub API
        github = GitHubClient(user.access_token)

        owner = repository.owner_name
        repo_name = repository.name

        files = asyncio.run(
            github.get_pull_request_files(
                owner,
                repo_name,
                pull_request.pr_number,
            )
        )

        # 6. Build patch
        patches = []

        for file in files:
            patch = file.get("patch")

            if patch:
                patches.append(
                    f"File: {file.get('filename')}\n\n{patch}"
                )

        full_patch = "\n\n".join(patches)

        if not full_patch:
            raise ValueError(
                "No patch data available for this pull request"
            )

        # 7. Gemini
        ai_client = AIClient()

        result = asyncio.run(
            ai_client.review_patch(full_patch)
        )

        # 8. Store AI result
        analysis.summary = result.get(
            "summary",
            ""
        )

        analysis.risk_score = result.get(
            "severity",
            "unknown"
        )

        issues = result.get(
            "issues",
            []
        )

        analysis.recommendations = "\n\n".join(
            [
                f"{issue.get('title', '')}: "
                f"{issue.get('description', '')}\n"
                f"Suggestion: {issue.get('suggestion', '')}"
                for issue in issues
            ]
        )

        analysis.missing_tests = any(
            issue.get("category") == "testing"
            for issue in issues
        )


        analysis.description_mismatch = False
        analysis.status = "completed"

        db.commit()
        db.refresh(analysis)

        # 9. Post AI review to GitHub PR
        issue_lines = []


        for issue in issues:
            severity = issue.get("severity", "low").upper()
            category = issue.get("category", "best_practice")


            issue_lines.append(
                f"""### {severity} — {issue.get("title", "Issue")}
**Category:** {category}


{issue.get("description", "")}


**Suggestion:** {issue.get("suggestion", "")}"""
            )


        issues_text = "\n\n".join(issue_lines)


        comment = f"""## 🤖 ReviewMate AI Review


### Summary


{analysis.summary}


### Overall Risk


**{analysis.risk_score.upper()}**


### Issues


{issues_text or "No issues found."}


---


*Generated automatically by ReviewMate.*
"""

        asyncio.run(
            github.create_pull_request_comment(
                owner,
                repo_name,
                pull_request.pr_number,
                comment,
            )
        )

        return {
            "analysis_id": analysis.id,
            "status": analysis.status,
            "risk_score": analysis.risk_score,
        }

    except Exception:
        db.rollback()

        analysis = (
            db.query(Analysis)
            .filter(
                Analysis.pull_request_id == pull_request_id
            )
            .first()
        )

        if analysis:
            analysis.status = "failed"
            db.commit()

        raise

    finally:
        db.close()
