from binance import AsyncClient


class BinanceAPI:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client: AsyncClient | None = None

    async def connect(self):
        self.client = await AsyncClient.create(
            self.api_key,
            self.api_secret,
            testnet=self.testnet,
        )
        return self

    async def disconnect(self):
        if self.client:
            await self.client.close_connection()
