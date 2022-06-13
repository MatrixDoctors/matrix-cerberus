import asyncio

from app.core.bot import BaseBotClient
from app.core.config import settings


class MatrixBotBackgroundRunner:
    def __init__(self):
        self.client = BaseBotClient(homeserver=settings.matrix_bot.homeserver)
        self.background_task = None

    async def start_bot(self):
        try:
            await self.client.login()
            await self.client.sync_forever(
                30000,
                since=self.client.next_batch,
                full_state=True,
                loop_sleep_time=2000,
            )
            await asyncio.sleep(1)
        except (asyncio.CancelledError, ValueError) as err:
            # Handles the ValueError received from BaseBotClient login function
            if isinstance(err, ValueError):
                print(err)
            await self.client.close()

    def create_background_task(self):
        print("Background task has started")
        self.background_task = asyncio.create_task(self.start_bot())

    async def cancel_background_task(self):
        self.background_task.cancel()
        print(f"Background Task is cancelled")


matrix_bot_runner = MatrixBotBackgroundRunner()
