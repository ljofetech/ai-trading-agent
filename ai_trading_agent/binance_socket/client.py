from binance import AsyncClient, BinanceSocketManager


class BinanceAPI:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client: AsyncClient | None = None
        self.socket_manager: BinanceSocketManager | None = None

    async def connect(self) -> "BinanceAPI":
        self.client = await AsyncClient.create(
            self.api_key,
            self.api_secret,
            testnet=self.testnet,
        )
        self.socket_manager = BinanceSocketManager(self.client)
        return self

    async def disconnect(self) -> None:
        if self.client:
            await self.client.close_connection()
            self.client = None
            self.socket_manager = None
