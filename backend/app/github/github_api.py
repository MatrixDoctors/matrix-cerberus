import gidgethub.aiohttp

from app.core.background_runner import matrix_bot_runner
from app.core.config import settings


class GithubAPI:
    def __init__(self, gh: gidgethub.aiohttp.GitHubAPI, username):
        self.username = username
        self.gh = gh
        self.default_role_level = self.role_level(settings.github.organisation_membership)

    def role_level(self, role: str):
        if role == "member":
            return 1
        elif role == "admin":
            return 2

    async def display_user(self):
        return self.user_id

    async def get_orgs_with_membership(self):
        list_of_orgs = []
        async for item in self.gh.getiter("/user/memberships/orgs"):
            if self.role_level(item["role"]) >= self.default_role_level:
                list_of_orgs.append(item["organization"]["login"])
        return list_of_orgs

    async def get_all_orgs(self):
        list_of_orgs = []
        async for item in self.gh.getiter(f"/user/{self.username}/orgs"):
            list_of_orgs.append(item)
        return list_of_orgs

    async def get_org_membership(self, org, user):
        resp = await self.gh.getitem(f"/orgs/{org}/memberships/{user}")
        return resp
