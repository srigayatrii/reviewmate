import asyncio

import app.models
from app.ai.client import AIClient
from app.models.analysis import Analysis
from app.db.database import SessionLocal
from app.github.client import GitHubClient
from app.models.pull_request import PullRequest
from app.models.pull_request_file import PullRequestFile
from app.models.repository import Repository
from app.models.webhook_event import WebhookEvent


def process_webhook_event(webhook_event_id: int):

    db = SessionLocal()

    try:

        webhook_event = (
            db.query(WebhookEvent)
            .filter(WebhookEvent.id == webhook_event_id)
            .first()
        )

        if not webhook_event:
            print(f"Webhook event {webhook_event_id} not found")
            return

        print(
            f"Processing webhook event "
            f"{webhook_event.id}: {webhook_event.event_type}"
        )

        # --------------------------------
        # Pull Request Events
        # --------------------------------

        if webhook_event.event_type == "pull_request":

            payload = webhook_event.payload

            pr_number = payload["pull_request"]["number"]

            repository = (
                db.query(Repository)
                .filter(
                    Repository.full_name ==
                    payload["repository"]["full_name"]
                )
                .first()
            )

            access_token = repository.owner.access_token

            github = GitHubClient(access_token)

            pr_data = asyncio.run(
                github.get_pull_request(
                    owner=repository.owner_name,
                    repository=repository.name,
                    pull_number=pr_number
                )
            )

            pr_files = asyncio.run(
                github.get_pull_request_files(
                    owner=repository.owner_name,
                    repository=repository.name,
                    pull_number=pr_number
                )
            )

            existing_pr = (
                db.query(PullRequest)
                .filter(
                    PullRequest.github_pr_id == pr_data["id"]
                )
                .first()
            )

            if existing_pr:

                existing_pr.title = pr_data["title"]
                existing_pr.description = pr_data["body"] or ""
                existing_pr.state = pr_data["state"]
                existing_pr.author = pr_data["user"]["login"]
                existing_pr.base_branch = pr_data["base"]["ref"]
                existing_pr.head_branch = pr_data["head"]["ref"]

                pull_request = existing_pr

                print(
                    f"Updated PR #{existing_pr.pr_number}"
                )

            else:

                new_pr = PullRequest(
                    github_pr_id=pr_data["id"],
                    pr_number=pr_data["number"],
                    title=pr_data["title"],
                    description=pr_data["body"] or "",
                    state=pr_data["state"],
                    author=pr_data["user"]["login"],
                    base_branch=pr_data["base"]["ref"],
                    head_branch=pr_data["head"]["ref"],
                    repository_id=repository.id,
                )

                db.add(new_pr)
                db.flush()

                pull_request = new_pr

                print(
                    f"Stored PR #{new_pr.pr_number}"
                )

            for file in pr_files:

                existing_file = (
                    db.query(PullRequestFile)
                    .filter(
                        PullRequestFile.pull_request_id == pull_request.id,
                        PullRequestFile.filename == file["filename"]
                    )
                    .first()
                )

                if existing_file:

                    existing_file.status = file["status"]
                    existing_file.additions = file["additions"]
                    existing_file.deletions = file["deletions"]
                    existing_file.changes = file["changes"]
                    existing_file.patch = file.get("patch")

                else:

                    db.add(
                        PullRequestFile(
                            filename=file["filename"],
                            status=file["status"],
                            additions=file["additions"],
                            deletions=file["deletions"],
                            changes=file["changes"],
                            patch=file.get("patch"),
                            pull_request_id=pull_request.id,
                        )
                    )
                patch = file.get("patch")
                if patch:
                    ai = AIClient()
                    analysis = asyncio.run(
                        ai.review_patch(patch)
                    )
                    recommendations = "\n\n".join(
                        issue["suggestion"]
                        for issue in analysis["issues"]
                    )
                    existing_analysis = (
                        db.query(Analysis)
                        .filter(
                            Analysis.pull_request_id == pull_request.id
                        )
                        .first()
                    )
                    if existing_analysis:
                        existing_analysis.summary = analysis["summary"]
                        existing_analysis.risk_score = analysis["severity"]
                        existing_analysis.recommendations = recommendations
                        existing_analysis.status = "completed"
                    else:
                        db.add(
                            Analysis(
                                summary=analysis["summary"],
                                risk_score=analysis["severity"],
                                recommendations=recommendations,
                                status="completed",
                                missing_tests=False,
                                description_mismatch=False,
                                pull_request_id=pull_request.id,
                            )
                        )
                    comment = f"""
                    ## 🤖 ReviewMate AI Review
                    ### Summary
                    {analysis["summary"]}
                    ### Risk
                    **{analysis["severity"].upper()}**
                    ### Recommendations
                    {recommendations}
                    """
                    asyncio.run(
                        github.create_pull_request_comment(
                            owner=repository.owner_name,
                            repository=repository.name,
                            pull_number=pr_number,
                            body=comment,
                        )
                    )
                    print("Posted AI review comment to GitHub")


            print(
                f"Stored {len(pr_files)} changed files"
            )

        webhook_event.status = "processed"

        db.commit()

        print(
            f"Webhook event {webhook_event.id} processed successfully"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()