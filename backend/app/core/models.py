from typing import Set, Dict, List, Optional

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


class RoomUrlObject(BaseModel):
    room_id: str
    use_once_only: bool


class ExternalUrlData(BaseModel):
    """
    Pydantic model used to evaluate account data for '<app_name>.external_url' event type.

    Attributes:
    'content' is a mapping between 'url_code' (string of length 8) and RoomUrlObject.
    """

    content: Dict[str, RoomUrlObject] = dict()


class RoomSpecificExternalUrl(BaseModel):
    """
    Pydantic class used to instantiate 'room_to_external_url_mapping' object for a particular room id in BaseBotClient class.
    """

    permanent: str = None
    temporary: Set[str] = set()


class RoomConditionsData(BaseModel):
    """
    RoomConditionsData class which handles conditions and data related to a specific room.

    Attributes:
    'github' has room invite conditions for GitHub users and sponsors.
    'patreon` has room invite conditions for Patreon users.
    """

    github: None = None
    patreon: None = None


class RoomSpecificData(BaseModel):
    """
    Pydantic model used to evaluate account data for `<app_name>.rooms.<room_id>` event type.
    """

    content: RoomConditionsData = RoomConditionsData()


class RoomMembershipContent(BaseModel):
    membership: str


class ClientEventData(BaseModel):
    content: RoomMembershipContent
    sender: str
    state_key: str


class RoomMembersData(BaseModel):
    chunk: List[ClientEventData]


class GlobalData(BaseModel):
    users: List[str] = []
    rooms: List[str] = []


class BotGlobalData(BaseModel):
    content: GlobalData = dict(GlobalData())


class GithubUserData(BaseModel):
    username: Optional[str] = None
    access_token: Optional[str] = None


class PatreonUserData(BaseModel):
    email: Optional[EmailStr] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class UserMappedData(BaseModel):
    github: GithubUserData = GithubUserData()
    patreon: PatreonUserData = PatreonUserData()


class UserData(BaseModel):
    content: UserMappedData = UserMappedData()
