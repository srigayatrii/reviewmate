from sqlalchemy.orm import Session

from app.github.client import GitHubClient
from app.models.repository import Repository
from app.models.user import User


class RepositoryService:

    def __init__(
        self,
        db: Session,
        current_user: User
    ):
        self.db = db
        self.current_user = current_user
        self.github_client = GitHubClient(
            current_user.access_token
        )

    async def sync_repositories(self):

        github_repositories = (
            await self.github_client.get_user_repositories()
        )

        print(f"GitHub returned {len(github_repositories)} repositories")

        for repo in github_repositories:
            print(repo["name"])

        synced_count = 0

        for repo in github_repositories:

            existing_repo = (
                self.db.query(Repository)
                .filter(
                    Repository.github_repo_id == repo["id"]
                )
                .first()
            )

            print(
                repo["name"],
                "Exists:",
                existing_repo is not None
            )

            if existing_repo:
                continue

            repository = Repository(
                github_repo_id=repo["id"],
                name=repo["name"],
                full_name=repo["full_name"],
                owner_name=repo["owner"]["login"],
                user_id=self.current_user.id
            )

            self.db.add(repository)
            synced_count += 1

        self.db.commit()

        return {
            "repositories_synced": synced_count
        }

    async def get_repositories(self):

        repositories = (
            self.db.query(Repository)
            .filter(
                Repository.user_id == self.current_user.id
            )
            .all()
        )

        return repositories
    async def get_repository(self, repository_id: int):
        repository = (
            self.db.query(Repository)
            .filter(
                Repository.id == repository_id,
                Repository.user_id == self.current_user.id
            )
            .first()
        )

        return repository
    async def connect_repository(self, repository_id: int):
        repository = (

            self.db.query(Repository)
            .filter(
                Repository.id == repository_id,
                Repository.user_id == self.current_user.id
           )
           .first()
        )
        if not repository:
            return {
                "message": "Repository not found"
            }
        repository.is_active = True
        self.db.commit()
        return {
            "message": "Repository connected successfully"
        }
    async def disconnect_repository(self, repository_id: int):
        repository = (
            self.db.query(Repository)
            .filter(
                Repository.id == repository_id,
                Repository.user_id == self.current_user.id
            )
            .first()
        )
        if not repository:
            return {
                "message": "Repository not found"
            }
        repository.is_active = False
        self.db.commit()
        return {
            "message": "Repository disconnected successfully"
        }






        