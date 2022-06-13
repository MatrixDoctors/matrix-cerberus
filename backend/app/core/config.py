import re
from pathlib import Path

import yaml
from pydantic import BaseSettings, RedisDsn, root_validator, validator


class RedisSettings(BaseSettings):
    uri: RedisDsn


class ServerSessionsSettings(BaseSettings):
    session_key: str
    expires_in: int


class MatrixBotSettings(BaseSettings):
    homeserver: str
    access_token: str

    # This checks if the user_id and homeserver match the rules set by the matrix spec.
    # This returns a dictionary instead of a MatrixBotSettings object
    @root_validator(pre=True)
    def validate(cls, values):
        homeserver = values.get("homeserver")

        if re.search(r"https?://", homeserver) is None:
            raise ValueError("Invalid homeserver")

        return values


class Settings(BaseSettings):

    redis: RedisSettings
    server_sessions: ServerSessionsSettings
    matrix_bot: MatrixBotSettings

    # Used to convert the dicitonary received from the root_validator of MatrixBotSettings class to an instance of the latter.
    @validator("matrix_bot")
    def validate_matrix_bot(cls, v, values):
        return MatrixBotSettings.parse_obj(v)

    @classmethod
    def from_yaml(cls, path_to_file):
        absolute_path_to_file = Path(path_to_file).absolute()

        try:
            with open(absolute_path_to_file) as f:
                yaml_settings = yaml.safe_load(f)
                return Settings.parse_obj(yaml_settings)
        except (IOError, ImportError) as err:
            print(f"Couldn't load config from file. Error: {err}")


settings = Settings.from_yaml("config.yml")
