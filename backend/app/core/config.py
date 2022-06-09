import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseSettings, RedisDsn

yaml_settings = None

# Load the config file present in the root directory (backend)
here = Path().absolute() / "config.yml"
with open(str(here)) as f:
    yaml_settings = yaml.safe_load(f)


class Settings(BaseSettings):
    redis_dsn: RedisDsn = yaml_settings["redis"]["uri"]
    session_key: str = yaml_settings["server_sessions"]["session_key"]
    session_expires_in: int = yaml_settings["server_sessions"]["expires_in"]


# Return only one instance of Settings for each call to 'get_settings'
@lru_cache()
def get_settings():
    return Settings()
