import aiohttp


class HttpClient:
    session: aiohttp.ClientSession = None

    def start_session(self):
        self.session = aiohttp.ClientSession()

    async def stop_session(self):
        await self.session.close()
        self.session = None


http_client = HttpClient()
