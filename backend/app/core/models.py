"""
This module consists of pydantic models and schema for:
i) All account data event types and
ii) Data required by other core modules.
"""

from typing import Any, Set, Dict, List, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


class ServerSessionData(BaseModel):
    """
    Pydantic model used to validate server session data.
    Created first during user login.
    """

    matrix_user: Optional[str] = None
    matrix_homeserver: Optional[str] = None
    github_user_id: Optional[str] = None
    github_access_token: Optional[str] = None
    patreon_user_id: Optional[str] = None
    patreon_access_token: Optional[str] = None
    patreon_refresh_token: Optional[str] = None
    patreon_expire_date: Optional[str] = None


class RoomUrlObject(BaseModel):
    room_id: str
    use_once_only: bool


class ExternalUrlData(BaseModel):
    """
    Pydantic model used to parse account data for '<app_name>.external_url' event type.

    Attributes:
    'content' is a mapping between 'url_code' (string of length 8) and RoomUrlObject.
    """

    content: Dict[str, RoomUrlObject] = dict()


class RoomSpecificExternalUrl(BaseModel):
    """
    Pydantic class used to parse 'room_to_external_url_mapping' data for a particular room id in BaseBotClient class.
    """

    permanent: str = None
    temporary: Set[str] = set()


class GithubRepositoryConditions(BaseModel):
    admin: bool = False
    write: bool = False
    read: bool = False


class GithubUserConditions(BaseModel):
    repos: Dict[str, GithubRepositoryConditions] = dict()
    sponsorship_tiers: Dict[str, bool] = dict()


class GithubOrganisationConditions(BaseModel):
    repos: Dict[str, GithubRepositoryConditions] = dict()
    teams: Dict[str, bool] = dict()
    sponsorship_tiers: Dict[str, bool] = dict()
    last_edited_by: str = None


class GithubConditions(BaseModel):
    orgs: Dict[str, GithubOrganisationConditions] = dict()
    users: Dict[str, GithubUserConditions] = dict()


class PatreonCampaignTier(BaseModel):
    title: str
    is_enabled: bool


class PatreonCampaignConditions(BaseModel):
    name: str = ""
    belongs_to: str = ""
    tiers: Dict[int, PatreonCampaignTier] = dict()
    enable_lifetime_support_cents: bool = False
    lifetime_support_cents: int = 0


class PatreonConditions(BaseModel):
    campaigns: Dict[int, PatreonCampaignConditions] = dict()


class RoomConditionsData(BaseModel):
    """
    RoomConditionsData class which handles conditions and data related to a specific room.

    Attributes:
    'disable_room_kick' makes the bot invite only and prevents it from removing joined users.
    'github' has room membership conditions for GitHub users, teams and sponsors.
    'patreon` has room membership conditions for Patreon users.
    """

    disable_room_kick: bool = False
    github: GithubConditions = GithubConditions()
    patreon: PatreonConditions = PatreonConditions()


class RoomSpecificData(BaseModel):
    """
    Pydantic model used to parse account data for `<app_name>.rooms.<room_id>` event type.
    """

    content: RoomConditionsData = RoomConditionsData()


class RoomMembershipContent(BaseModel):
    membership: str


class ClientEventData(BaseModel):
    content: RoomMembershipContent
    sender: str
    state_key: str


class RoomMembersData(BaseModel):
    """
    Room Members data for the 'rooms/{roomId}/members' endpoint.
    """

    chunk: List[ClientEventData]


class GlobalData(BaseModel):
    users: List[str] = []
    rooms: List[str] = []


class BotGlobalData(BaseModel):
    """
    Pydantic model used to parse account data for `<app_name>.global_data` event type.
    """

    content: GlobalData = dict(GlobalData())


class GithubUserData(BaseModel):
    username: Optional[str] = None
    access_token: Optional[str] = None


class PatreonUserData(BaseModel):
    email: Optional[EmailStr] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expire_date: Optional[datetime] = None


class UserMappedData(BaseModel):
    github: GithubUserData = GithubUserData()
    patreon: PatreonUserData = PatreonUserData()


class UserData(BaseModel):
    """
    Pydantic model used to parse account data for `<app_name>.user.<user_id>` event type.
    """

    content: UserMappedData = UserMappedData()
