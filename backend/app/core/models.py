from typing import Set, Dict, List, Optional

from pydantic import BaseModel


class ServerSessionData(BaseModel):
    """
    Pydantic model used to validate server session data.
    Created first during user login.
    """

    matrix_user: Optional[str] = None
    matrix_homeserver: Optional[str] = None
    github_access_token: Optional[str] = None
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
    permanent: str = None
    temporary: Set[str] = set()


class RoomConditionsData(BaseModel):
    """
    RoomConditionsData class which handles conditions and data related to a specific room.

    Attributes:
    'external_url' consists of "permanent" and "single-use" external url tokens.
    'github' has room invite conditions for GitHub users and sponsors.
    'patreon` has room invite conditions for Patreon users.
    """

    external_url: RoomSpecificExternalUrl = RoomSpecificExternalUrl()


class RoomSpecificData(BaseModel):
    """
    Pydantic model used to evaluate account data for `<app_name>.rooms.<room_id>` event type.
    """

    content: RoomConditionsData = RoomConditionsData()
