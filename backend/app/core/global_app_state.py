from app.core.background_runner import MatrixBotBackgroundRunner
from app.core.bot import BaseBotClient
from app.core.config import settings
from app.core.http_client import HttpClient
from app.core.sessions import RedisSessionStorage, SessionCookie


class AppState:
    def __init__(self):
        self.settings = settings
        self.http_client = HttpClient()
        self.session_storage = RedisSessionStorage(self.settings.redis.uri)

        self.server_session = SessionCookie(
            session_storage=self.session_storage,
            session_key=self.settings.server_sessions.session_key,
            expires_in=self.settings.server_sessions.expires_in,
        )

        self.bot_client = BaseBotClient(
            homeserver=self.settings.matrix_bot.homeserver,
            app_name=self.settings.app_name,
            http_client=self.http_client,
        )

        self.matrix_bot_runner = MatrixBotBackgroundRunner(
            client=self.bot_client,
            access_token=self.settings.matrix_bot.access_token,
            session_storage=self.session_storage,
        )

    async def setup_state(self):
        await self.http_client.start_session()
        self.matrix_bot_runner.create_background_task()

    async def close(self):
        await self.http_client.stop_session()
        await self.matrix_bot_runner.cancel_background_task()


app_state = AppState()
