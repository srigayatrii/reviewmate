import asyncio

import app.models
from app.models.pull_request import PullRequest
from app.db.database import SessionLocal
from app.github.client import GitHubClient
from app.models.webhook_event import WebhookEvent
from app.models.repository import Repository


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

        # -------------------------------
        # Pull Request Events
        # -------------------------------

        if webhook_event.event_type == "pull_request":

            payload = webhook_event.payload

            action = payload["action"]

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

                print(
                    f"Stored PR #{new_pr.pr_number}"
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