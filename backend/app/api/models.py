from typing import Any

from pydantic import BaseModel


class OpenIdInfo(BaseModel):
    """
    Pydantic model used to validate Open ID token details received from the client side.
    It will be used for authenticating a matrix user.
    """

    access_token: str
    expires_in: int
    matrix_server_name: str
    token_type: str


class ExternalUrlInfo(BaseModel):
    """
    Pydantic model used to validate external url information required to generate a url.
    """

    room_id: str
    use_once_only: bool


class OAuthCode(BaseModel):
    """
    Validates the POST body for the /api/github/login endpoint.
    """

    code: str


class OwnerField(BaseModel):
    parent: str
    child: str = None


class RoomConditions(BaseModel):
    """
    Pydantic model used to parse data received from 'room' account data event before it is sent to the client-side.
    """

    type: str
    third_party_account: str
    owner: OwnerField
    condition_type: str
    data: Any = None
