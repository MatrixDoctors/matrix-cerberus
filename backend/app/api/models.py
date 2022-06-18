from pydantic import BaseModel


class OpenIdInfo(BaseModel):
    access_token: str
    expires_in: int
    matrix_server_name: str
    token_type: str
