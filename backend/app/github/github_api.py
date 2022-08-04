import gidgethub
import gidgethub.aiohttp


class GithubAPI:
    def __init__(self, gh: gidgethub.aiohttp.GitHubAPI, username: str, default_role: str):
        self.username = username
        self.gh = gh
        self.default_role_level = self.role_level(default_role)

    def role_level(self, role: str):
        if role == "member":
            return 1
        elif role == "admin":
            return 2

    async def display_user(self):
        return self.username

    async def get_orgs_with_membership(self):
        """
        Fetches all the organization memberships for the current user.
        """
        list_of_orgs = []
        async for item in self.gh.getiter("/user/memberships/orgs"):
            if self.role_level(item["role"]) >= self.default_role_level:
                list_of_orgs.append(item["organization"]["login"])
        return list_of_orgs

    async def get_all_orgs(self):
        """
        Get all orgs where the user is either an owner, member or collaborator (has support for Github apps)
        """
        list_of_orgs = []
        async for item in self.gh.getiter(f"/user/{self.username}/orgs"):
            list_of_orgs.append(item)
        return list_of_orgs

    async def org_membership_of_user(self, org, user):
        resp = await self.gh.getitem(f"/orgs/{org}/memberships/{user}")
        return resp

    async def get_repos_in_an_org(self, org):
        list_of_repos = []
        async for item in self.gh.getiter(f"/orgs/{org}/repos"):
            list_of_repos.append(item["name"])
        return list_of_repos

    async def get_individual_repos(self):
        """
        Get repositories owned by the current user
        """
        list_of_repos = []
        async for item in self.gh.getiter(f"/user/repos?affiliation=owner"):
            list_of_repos.append(item["name"])
        return list_of_repos

    async def get_teams_in_an_org(self, org):
        teams = {}
        async for item in self.gh.getiter(f"/orgs/{org}/teams"):
            teams[item["slug"]] = item["name"]
        return teams

    async def is_team_member(self, org, team_slug, user):
        try:
            resp = await self.gh.getitem(f"/orgs/{org}/teams/{team_slug}/memberships/{user}")
        except gidgethub.BadRequest:
            return False
        return True

    async def repo_permissions(self, owner, repo, user):
        resp = await self.gh.getitem(f"/repos/{owner}/{repo}/collaborators/{user}/permission")
        return resp["permission"]

    async def get_sponsorship_tiers_for_user(self, user):
        query = """
        query ($user:String!, $number_of_tiers_to_fetch:Int!)
        {
            user(login: $user) {
                sponsorsListing {
                    tiers(first: $number_of_tiers_to_fetch) {
                        nodes {
                            name
                        }
                    }
                }
            }
        }
        """

        resp = await self.gh.graphql(query=query, user=user, number_of_tiers_to_fetch=10)

        if resp["organization"]["sponsorsListing"] is None:
            return []

        sponsor_tiers = []
        for tier in resp["user"]["sponsorsListing"]["tiers"]["nodes"]:
            sponsor_tiers.append(tier["name"])

        return sponsor_tiers

    async def get_sponsorship_tiers_for_org(self, org):
        query = """
        query ($org:String!, $number_of_tiers_to_fetch:Int!)
        {
            organization(login: $org) {
                sponsorsListing {
                    tiers(first: $number_of_tiers_to_fetch) {
                        nodes {
                            name
                        }
                    }
                }
            }
        }
        """

        resp = await self.gh.graphql(query=query, org=org, number_of_tiers_to_fetch=10)

        if resp["organization"]["sponsorsListing"] is None:
            return []

        sponsor_tiers = []
        for tier in resp["organization"]["sponsorsListing"]["tiers"]["nodes"]:
            sponsor_tiers.append(tier["name"])

        return sponsor_tiers

    async def user_sponsored_at_tier(self, user):
        query = """
        query ($user:String!)
        {
            user(login: $user) {
                sponsorshipForViewerAsSponsor {
                    tier {
                        name
                    }
                }
            }
        }
        """
        resp = await self.gh.graphql(query=query, user=user)
        sponsorship_data = resp["user"]["sponsorshipForViewerAsSponsor"]
        if sponsorship_data is None:
            return None
        return sponsorship_data["tier"]["name"]

    async def org_sponsored_at_tier(self, org):
        query = """
        query ($org:String!)
        {
            organization(login: $org) {
                sponsorshipForViewerAsSponsor {
                    tier {
                        name
                    }
                }
            }
        }
        """
        resp = await self.gh.graphql(query=query, org=org)
        sponsorship_data = resp["organization"]["sponsorshipForViewerAsSponsor"]
        if sponsorship_data is None:
            return None
        return sponsorship_data["tier"]["name"]
