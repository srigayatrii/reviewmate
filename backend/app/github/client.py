import httpx


class GitHubClient:

    BASE_URL = "https://api.github.com"

    def __init__(self, access_token: str):

        self.access_token = access_token

        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        }

    async def get_user_repositories(self):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/user/repos",
                headers=self.headers,
            )

        response.raise_for_status()

        return response.json()

    async def get_pull_request(
        self,
        owner: str,
        repository: str,
        pull_number: int
    ):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pull_number}",
                headers=self.headers,
            )

        response.raise_for_status()

        return response.json()

    async def get_pull_request_files(
        self,
        owner: str,
        repository: str,
        pull_number: int
    ):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pull_number}/files",
                headers=self.headers,
            )

        response.raise_for_status()

        return response.json()

    async def get_pull_request_commits(
        self,
        owner: str,
        repository: str,
        pull_number: int
    ):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repository}/pulls/{pull_number}/commits",
                headers=self.headers,
            )

        response.raise_for_status()

        return response.json()