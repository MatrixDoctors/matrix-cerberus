from typing import Optional

from pydantic import BaseModel


class ServerSessionData(BaseModel):
    matrix_user: Optional[str] = None
    github_access_token: Optional[str] = None
    patreon_access_token: Optional[str] = None
