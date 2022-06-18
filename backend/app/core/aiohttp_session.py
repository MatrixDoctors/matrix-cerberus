import aiohttp


class AioHttpSession:
    session = None

    @classmethod
    def start_session(cls):
        cls.session = aiohttp.ClientSession()

    @classmethod
    async def stop_session(cls):
        await cls.session.close()
