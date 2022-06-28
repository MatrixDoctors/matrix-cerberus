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


class GithubCode(BaseModel):

    code: str
