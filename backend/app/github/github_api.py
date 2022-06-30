import gidgethub.aiohttp

from app.core.background_runner import matrix_bot_runner


class GithubAPI:
    def __init__(self, gh: gidgethub.aiohttp.GitHubAPI, user_id):
        self.user_id = user_id
        self.gh = gh

    async def display_user(self):
        return self.user_id
