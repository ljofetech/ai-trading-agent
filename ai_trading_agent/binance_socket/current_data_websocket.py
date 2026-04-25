import os
import asyncio

from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from binance_socket.client import BinanceAPI

# Retrieve Binance API credentials from environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


async def stream_futures_candle(symbol: str, interval: str):
    """
    Stream real-time futures candlestick data for a given symbol and interval
    via Binance WebSocket.
    """
    # Initialize Binance API client (using live futures, not testnet)
    binance = BinanceAPI(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=False)
    # Establish connection and create socket manager
    await binance.connect()

    try:
        # Build the stream name required by Binance: e.g., "btcusdt@kline_15m"
        stream_name = f"{symbol.lower()}@kline_{interval}"

        # Create a multiplex socket for the futures kline stream
        socket = binance.socket_manager.futures_multiplex_socket([stream_name])

        # Use async context manager to ensure clean connection handling
        async with socket as stream:
            # Infinite loop to continuously receive updates
            while True:
                # Wait for the next message from the WebSocket
                msg = await stream.recv()

                # Extract the candlestick data from the message payload
                kline = msg["data"]["k"]

                # Format the raw data into a clean dictionary
                candle = {
                    # Convert open time from milliseconds to datetime object
                    "open_time": datetime.fromtimestamp(kline["t"] / 1000),
                    "open": float(kline["o"]),  # Opening price
                    "high": float(kline["h"]),  # Highest price during period
                    "low": float(kline["l"]),  # Lowest price during period
                    "close": float(kline["c"]),  # Current/latest price
                    "volume": float(kline["v"]),  # Trading volume
                    # Convert close time from milliseconds to datetime object
                    "close_time": datetime.fromtimestamp(kline["T"] / 1000),
                    "closed": kline[
                        "x"
                    ],  # True if candle is final, False if still updating
                }

                # Output the candle data to the console
                print(candle)

    except Exception as e:
        # Handle any WebSocket or connection errors
        print(f"WebSocket error: {e}")

    finally:
        # Always close the Binance client connection when done
        await binance.disconnect()


# if __name__ == "__main__":
#     # Run the async function for BTCUSDT with 15-minute candles
#     asyncio.run(stream_futures_candle("BTCUSDT", "15m"))
