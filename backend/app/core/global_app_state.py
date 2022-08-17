from pathlib import Path

import yaml

from app.core.background_runner import MatrixBotBackgroundRunner
from app.core.bot import BaseBotClient
from app.core.config import Settings
from app.core.http_client import HttpClient
from app.core.sessions import RedisSessionStorage, SessionCookie
from app.matrix.background_validator import BackgroundValidater


class AppState:
    def __init__(self, settings_file: str = "config.yml"):
        self.settings = self.get_settings_from_yaml(settings_file)
        self.session_storage = RedisSessionStorage(self.settings.redis.uri)
        self.server_session = SessionCookie(
            session_storage=self.session_storage,
            session_key=self.settings.server_sessions.session_key,
            expires_in=self.settings.server_sessions.expires_in,
        )
        self.http_client = HttpClient()
        self.bot_client = None
        self.matrix_bot_runner = None
        self.background_validator = None

    async def setup_state(self):
        """
        Variables which store state will be initialised here.
        """
        self.bot_client = BaseBotClient(
            homeserver=self.settings.matrix_bot.homeserver,
            app_name=self.settings.app_name,
            http_client=self.http_client,
            min_power_level=self.settings.matrix_bot.min_power_level,
        )

        self.matrix_bot_runner = MatrixBotBackgroundRunner(
            client=self.bot_client,
            access_token=self.settings.matrix_bot.access_token,
            session_storage=self.session_storage,
        )

    async def delete_state(self):
        """
        Clears the variables and their states
        """
        self.bot_client = None
        self.matrix_bot_runner = None

    async def start_session(self):
        """
        All the background running tasks and session variables will be managed here.
        """
        await self.matrix_bot_runner.initialise_bot()

        await self.http_client.start_session()
        await self.matrix_bot_runner.create_background_task()

        self.background_validator = BackgroundValidater(
            bot_client=self.bot_client,
            http_client=self.http_client,
            github_default_role=self.settings.github.organisation_membership,
        )
        await self.background_validator.create_background_task()

    async def close_session(self):
        await self.http_client.stop_session()
        await self.matrix_bot_runner.cancel_background_task()
        await self.background_validator.cancel_background_task()

    def get_settings_from_yaml(cls, path_to_file):
        absolute_path_to_file = Path(path_to_file).absolute()
        try:
            with open(absolute_path_to_file) as f:
                yaml_settings = yaml.safe_load(f)
                return Settings.parse_obj(yaml_settings)
        except (IOError, ImportError) as err:
            print(f"Couldn't load config from file. Error: {err}")
