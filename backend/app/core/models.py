from typing import Dict, List, Optional

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
