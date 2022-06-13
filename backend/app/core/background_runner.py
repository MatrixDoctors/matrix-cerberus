import asyncio
import json

from app.core.bot import BaseBotClient
from app.core.config import settings


class BackgroundRunner:
    def __init__(self):
        self.client = BaseBotClient.get_bot_client()
        self.background_task = None

    async def start_bot(self):
        try:
            with open(settings.matrix_bot.next_batch_token_file, "r") as f:
                data = json.load(f)
                self.client.next_batch = data["next_batch_token"]
        except IOError:
            print(f"Couldn't load next batch token from file.")
        except json.JSONDecodeError:
                print("Couldn't read JSON file; overwriting")

        try:
            await self.client.login()
            await self.client.sync_forever(
                30000,
                since=self.client.next_batch,
                full_state=True,
                loop_sleep_time=2000,
            )
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            await self.client.close()

    def create_background_task(self):
        print("Background task has started")
        self.background_task = asyncio.create_task(self.start_bot())

    async def cancel_background_task(self):
        self.background_task.cancel()
        print(f"Background Task is cancelled")
        try:
            with open(settings.matrix_bot.next_batch_token_file, "w") as f:
                json.dump(
                    {
                        "next_batch_token": self.client.next_batch,
                    },
                    f,
                )
        except IOError as err:
            print(f"Couldn't load next batch token from file. Error: {err}")


runner = BackgroundRunner()
