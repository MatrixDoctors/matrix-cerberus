import json

GITHUB_USER_ID = "p0tato"
GITHUB_ACCESS_TOKEN = "some_access_token"


class TestClass:
    @staticmethod
    def _load_response(filename):
        with open(filename, encoding="utf-8") as f:
            return json.loads(f.read())

    @property
    def org_membership_response(self):
        resp = self._load_response("tests/data/github/org_memberships_response.json")
        return resp

    @property
    def repos_response(self):
        return self._load_response("tests/data/github/repos_response.json")

    @property
    def teams_response(self):
        return self._load_response("tests/data/github/teams_response.json")

    @property
    def repo_permissions(self):
        return self._load_response("tests/data/github/repo_permissions_response.json")

    async def test_display_user(self, github_api):
        assert github_api.username == GITHUB_USER_ID

    async def test_get_orgs_with_membership(self, mock_server, github_api):
        # When membership is 'member'
        github_api.default_role_level = github_api.role_level("member")

        mock_server.get(
            url="https://api.github.com/user/memberships/orgs",
            status=200,
            payload=self.org_membership_response,
        )

        resp = await github_api.get_orgs_with_membership()
        assert resp == ["matrix-cerberus", "github"]

        # When membership is 'admin'
        github_api.default_role_level = github_api.role_level("admin")

        mock_server.get(
            url="https://api.github.com/user/memberships/orgs",
            status=200,
            payload=self.org_membership_response,
        )

        resp = await github_api.get_orgs_with_membership()
        assert len(resp) == 1
        assert resp == ["matrix-cerberus"]

    async def test_get_repos_in_an_org(self, mock_server, github_api):
        org = "octocat"
        mock_server.get(
            url=f"https://api.github.com/orgs/{org}/repos", status=200, payload=self.repos_response
        )

        resp = await github_api.get_repos_in_an_org(org)
        assert resp == ["Hello-World"]

    async def test_get_individual_repos(self, mock_server, github_api):
        mock_server.get(
            url=f"https://api.github.com/user/repos?affiliation=owner",
            status=200,
            payload=self.repos_response,
        )

        resp = await github_api.get_individual_repos()
        assert resp == ["Hello-World"]

    async def test_get_teams_in_an_org(self, mock_server, github_api):
        org = "octocat"
        mock_server.get(
            url=f"https://api.github.com/orgs/{org}/teams", status=200, payload=self.teams_response
        )

        resp = await github_api.get_teams_in_an_org(org)
        assert resp == {"justice-league": "Justice League"}

    async def test_is_team_member(self, mock_server, github_api):
        org = "octocat"
        team_slug = "justice-league"
        user = GITHUB_USER_ID

        mock_server.get(
            url=f"https://api.github.com/orgs/{org}/teams/{team_slug}/memberships/{user}",
            status=200,
            payload={},
        )

        resp = await github_api.is_team_member(org, team_slug, user)
        assert resp == True

        mock_server.get(
            url=f"https://api.github.com/orgs/{org}/teams/{team_slug}/memberships/{user}",
            status=200,
            payload={},
        )

        resp = await github_api.is_team_member(org, team_slug, user)
        assert resp == True

    async def test_repo_permissions(self, mock_server, github_api):
        owner = "octocat"
        repo = "hello-world"
        user = GITHUB_USER_ID

        mock_server.get(
            url=f"https://api.github.com/repos/{owner}/{repo}/collaborators/{user}/permission",
            status=200,
            payload=self.repo_permissions,
        )

        resp = await github_api.repo_permissions(owner, repo, user)
        assert resp == "admin"
