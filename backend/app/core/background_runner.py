"""
Background task that provides classes and methods required to start and stop a matrix bot client.

Any methods that are requried to be run before bot startup or after bot shutdown go here.
"""

import asyncio

from app.core.bot import BaseBotClient
from app.core.sessions import RedisSessionStorage


class MatrixBotBackgroundRunner:
    def __init__(
        self,
        client: BaseBotClient,
        access_token: str,
        session_storage: RedisSessionStorage,
    ):
        self.client = client
        self.background_task = None
        self.session_storage = session_storage
        self.access_token = access_token

    async def initialise_bot(self):
        # Fetch next batch token stored in redis
        self.client.next_batch = self.session_storage["next_batch_token"]
        await self.client.login(access_token=self.access_token)
        await self.client.create_room_to_external_url_mapping()

    async def start_sync(self):
        try:
            await self.client.sync_forever(
                30000,
                since=self.client.next_batch,
                full_state=True,
                loop_sleep_time=2000,
            )
            # Sleep time of one second required to close the client session, reason needs to be found.
            await asyncio.sleep(1)
        except (asyncio.CancelledError, ValueError) as err:
            # Handles the ValueError received from BaseBotClient login function
            if isinstance(err, ValueError):
                print(err)
            await self.client.close()

    async def create_background_task(self):
        print("Background task has started")
        await self.initialise_bot()
        self.background_sync_task = asyncio.create_task(self.start_sync())

    async def cancel_background_task(self):
        # Store next batch token in redis, returns None if not found.
        self.session_storage["next_batch_token"] = self.client.next_batch

        self.background_sync_task.cancel()
        print(f"Background Task is cancelled")
