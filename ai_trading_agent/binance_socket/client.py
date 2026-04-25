from binance import AsyncClient, BinanceSocketManager


class BinanceAPI:
    """
    Wrapper class for the Binance AsyncClient and WebSocket manager.
    Provides a simplified interface to connect, disconnect, and access both
    REST API and WebSocket streaming functionality.
    """

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the BinanceAPI instance.

        Args:
            api_key: Binance API key (from environment or config)
            api_secret: Binance API secret (from environment or config)
            testnet: If True, use Binance Futures Testnet; if False, use live exchange
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

        # Will be set after connect() is called
        self.client: AsyncClient | None = None
        # Will be set after connect() is called; used to create WebSocket streams
        self.socket_manager: BinanceSocketManager | None = None

    async def connect(self) -> "BinanceAPI":
        """
        Asynchronously create the AsyncClient and initialize the socket manager.

        This method must be called before making any API requests or opening WebSocket streams.

        Returns:
            Self (the BinanceAPI instance) to allow method chaining.
        """
        # Create the asynchronous REST client
        self.client = await AsyncClient.create(
            self.api_key,
            self.api_secret,
            testnet=self.testnet,  # Routes to either live or testnet endpoints
        )
        # Initialize the WebSocket manager using the created client
        self.socket_manager = BinanceSocketManager(self.client)
        return self

    async def disconnect(self) -> None:
        """
        Cleanly close the underlying REST client connection and reset attributes.

        Should be called when the API instance is no longer needed to release resources.
        """
        if self.client:
            # Close the connection to prevent resource leaks
            await self.client.close_connection()
            # Reset to None to indicate the client is no longer available
            self.client = None
            self.socket_manager = None
