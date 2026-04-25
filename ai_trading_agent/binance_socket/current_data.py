import os
import asyncio

from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (API keys)
load_dotenv()

from binance_socket.client import BinanceAPI

# Retrieve Binance API credentials from environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


async def get_current_futures_candle(symbol: str, interval: str):
    """
    Fetch the latest (current, incomplete) futures candlestick via REST API.
    The output format is identical to the WebSocket version to ensure compatibility.
    """
    # Initialize the Binance API client (live futures, not testnet)
    binance = BinanceAPI(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=False)
    # Establish the connection to the Binance REST API
    await binance.connect()

    try:
        # Request only the most recent kline (limit=1). This returns the
        # candle that is currently forming (not yet closed).
        klines = await binance.client.futures_klines(
            symbol=symbol, interval=interval, limit=1  # Only fetch the latest candle
        )

        # The REST response for futures klines is a list of lists:
        # [
        #   [
        #     0: open_time (ms),
        #     1: open price,
        #     2: high price,
        #     3: low price,
        #     4: close price (current last price),
        #     5: volume,
        #     6: close_time (ms),
        #     7: quote asset volume,
        #     8: number of trades,
        #     9: taker buy base volume,
        #     10: taker buy quote volume,
        #     11: ignore
        #   ]
        # ]
        k = klines[0]  # Extract the single (latest) candle

        # Build a dictionary with the same structure as the original WebSocket output
        candle = {
            # Convert open_time from milliseconds to a datetime object
            "open_time": datetime.fromtimestamp(
                k[0] / 1000
            ),  # equivalent to kline["t"]
            "open": float(k[1]),  # kline["o"]
            "high": float(k[2]),  # kline["h"]
            "low": float(k[3]),  # kline["l"]
            "close": float(k[4]),  # kline["c"] (current price)
            "volume": float(k[5]),  # kline["v"]
            # Convert close_time from milliseconds to a datetime object
            "close_time": datetime.fromtimestamp(
                k[6] / 1000
            ),  # equivalent to kline["T"]
            # Because we fetched the current (open) candle, "closed" is always False
            "closed": False,  # equivalent to kline["x"] = False
        }

        # Print the formatted candle data
        print(candle)

        return candle

    except Exception as e:
        # Handle any REST API errors (e.g., network issues, invalid symbol)
        print(f"REST API error: {e}")

    finally:
        # Always close the Binance client connection to clean up resources
        await binance.disconnect()


# if __name__ == "__main__":
#     # Execute the async function: fetch current 15-minute candle for BTCUSDT futures
#     asyncio.run(get_current_futures_candle("BTCUSDT", "15m"))
