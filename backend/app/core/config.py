import re
from pathlib import Path

import yaml
from pydantic import BaseModel, BaseSettings, RedisDsn, root_validator, validator


class RedisSettings(BaseModel):
    uri: RedisDsn


class ServerSessionsSettings(BaseModel):
    session_key: str
    expires_in: int


class MatrixBotSettings(BaseModel):
    homeserver: str
    access_token: str
    min_power_level: int
    bg_validation_cooldown: int

    # This checks if the homeserver url is valid or not.
    @root_validator(pre=True)
    def validate(cls, values):
        homeserver = values.get("homeserver")

        if re.search(r"(https|http)?://", homeserver) is None:
            raise ValueError("Invalid homeserver")

        return values


class GitHubAppCredentials(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str
    organisation_membership: str


class PatreonAppCredentials(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str


class LoggerSettings(BaseModel):
    path: str
    filename: str
    rotation: str
    retention: str
    use_stdout: bool
    filepath: str = None

    @validator("filepath", always=True)
    def validate_filepath(cls, v, values):
        if values["use_stdout"]:
            return v

        path_to_file_directory = Path(values["path"]).absolute()
        path_to_file = Path.joinpath(path_to_file_directory, values["filename"])

        if path_to_file_directory.exists():
            return str(path_to_file)
        else:
            raise ValueError("Path does not exist.")


class Settings(BaseSettings):

    app_name: str
    redis: RedisSettings
    server_sessions: ServerSessionsSettings
    matrix_bot: MatrixBotSettings
    github: GitHubAppCredentials
    patreon: PatreonAppCredentials
    logging: LoggerSettings

    # Used to convert the dicitonary received from the root_validator of MatrixBotSettings class to an instance of the latter.
    @validator("matrix_bot")
    def validate_matrix_bot(cls, v, values):
        return MatrixBotSettings.parse_obj(v)

    def from_yaml(cls, path_to_file):
        absolute_path_to_file = Path(path_to_file).absolute()
        try:
            with open(absolute_path_to_file) as f:
                yaml_settings = yaml.safe_load(f)
                return Settings.parse_obj(yaml_settings)
        except (IOError, ImportError) as err:
            print(f"Couldn't load config from file. Error: {err}")
