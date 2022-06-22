from typing import Dict, Optional

from pydantic import BaseModel


class ServerSessionData(BaseModel):
    """
    Pydantic model used to validate server session data.
    Created first during user login.
    """

    matrix_user: Optional[str] = None
    github_access_token: Optional[str] = None
    patreon_access_token: Optional[str] = None


class RoomUrlObject(BaseModel):
    room_id: str
    use_once_only: bool


class ExternalUrlData(BaseModel):
    content: Dict[str, RoomUrlObject]
