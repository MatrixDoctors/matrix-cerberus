import aiohttp
from fastapi import HTTPException

from app.core.models import PatreonCampaignConditions, PatreonCampaignTier


class PatreonAPI:
    def __init__(self, email: str, access_token: str, session: aiohttp.ClientSession):
        self.email = email
        self.access_token = access_token
        self.session = session

    async def campaign_information(self):
        url = f"https://www.patreon.com/api/oauth2/v2/campaigns?"
        scopes = "fields[campaign]=created_at,creation_name&include=tiers&fields[tier]=title"
        scopes.replace("[", "%5B")
        scopes.replace("]", "%5D")

        url = url + scopes
        headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}

        async with self.session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=422, detail="Error fetching patreon details")
            campaign_data = await resp.json()

            tiers = {
                tier["id"]: PatreonCampaignTier(title=tier["attributes"]["title"], is_enabled=False)
                for tier in campaign_data["included"]
            }
            patreon_campaign_conditions = PatreonCampaignConditions(
                name=campaign_data["data"][0]["attributes"]["creation_name"],
                belongs_to=self.email,
                tiers=tiers,
                enable_lifetime_support_cents=False,
                lifetime_support_cents=0,
            )

            data = {
                "id": campaign_data["data"][0]["id"],
                "attributes": patreon_campaign_conditions.dict(),
            }
            return data

    async def user_memberships(self):
        url = f"https://www.patreon.com/api/oauth2/v2/identity?"
        scopes = "fields[user]=about,created,email,first_name,last_name,full_name&include=memberships&fields[member]=campaign_lifetime_support_cents"
        scopes.replace("[", "%5B")
        scopes.replace("]", "%5D")

        url = url + scopes
        headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}

        async with self.session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=422, detail="Error fetching patreon details")

            user_data = await resp.json()
            membership_list = []
            for membership in user_data["included"]:
                member_id = membership["id"]
                data = await self.membership_details(member_id)
                membership_list.append(data)

            return membership_list

    async def membership_details(self, member_id: str):
        url = f"https://www.patreon.com/api/oauth2/v2/members/{member_id}?"
        scopes = "fields[member]=currently_entitled_amount_cents,patron_status&include=currently_entitled_tiers&fields[tier]=title"
        scopes.replace("[", "%5B")
        scopes.replace("]", "%5D")

        url = url + scopes
        headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}

        async with self.session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=422, detail="Error fetching patreon details")
            membership_data = await resp.json()

            tiers = []
            for tier in membership_data["included"]:
                tiers.append(tier["attributes"]["title"])

            data = {
                "tiers": tiers,
                "currently_entitled_amount_cents": membership_data["data"]["attributes"][
                    "currently_entitled_amount_cents"
                ],
                "patron_status": membership_data["data"]["attributes"]["patron_status"],
            }

            return data
