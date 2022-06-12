from pathlib import Path

import yaml
from pydantic import BaseSettings, RedisDsn, validator

class RedisSettings(BaseSettings):
    uri: RedisDsn

class ServerSessionsSettings(BaseSettings):
    session_key: str
    expires_in: int

class Settings(BaseSettings):
    
    redis: RedisSettings
    server_sessions: ServerSessionsSettings

    @classmethod
    def from_yaml(cls, path_to_file):
        absolute_path_to_file = Path(path_to_file).absolute()

        try:
            with open(absolute_path_to_file) as f:
                yaml_settings = yaml.safe_load(f)
                return Settings.parse_obj(yaml_settings)
        except (IOError, ImportError) as err:
            print(f"Couldn't load config from file. Error: {err}")

settings = Settings.from_yaml('config.yml')