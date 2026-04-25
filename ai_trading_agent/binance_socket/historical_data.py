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


async def get_historical_klines_range(
    symbol: str, interval: str, start_date: str, end_date: str
):
    """
    Fetch historical futures candlestick data for a given symbol and interval
    between two specified dates using Binance REST API.

    Args:
        symbol: Trading pair (e.g., "BTCUSDT")
        interval: Candle interval (e.g., "15m", "1h", "1d")
        start_date: Start time string (e.g., "1 Jan 2024", "1d ago UTC")
        end_date: End time string (e.g., "now UTC", "2 Jan 2024")

    Returns:
        List of klines, each a list of raw data as returned by Binance.
    """
    # Initialize Binance API client (live futures, not testnet)
    binance = BinanceAPI(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=False)
    # Establish the connection to Binance REST API
    await binance.connect()

    try:
        # Request historical klines for the specified date range
        # This endpoint handles pagination automatically and returns all candles
        # between start_date and end_date.
        klines = await binance.client.futures_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_date,  # Flexible date string accepted by Binance
            end_str=end_date,  # Can be "now UTC" or a specific date
        )
        return klines
    finally:
        # Ensure the client connection is closed even if an error occurs
        await binance.disconnect()


# async def main():
#     """
#     Main async function to demonstrate fetching historical klines.
#     Prints the number of candles retrieved and a summary of each.
#     """
#     # Define the parameters for the historical data request
#     symbol = "BTCUSDT"  # Bitcoin / Tether futures pair
#     interval = "15m"  # 15‑minute candles
#     start_date = "1d ago UTC"  # Start from 1 day ago (relative time)
#     end_date = "now UTC"  # Up to the current moment

#     try:
#         # Fetch the historical klines
#         klines = await get_historical_klines_range(
#             symbol,
#             interval,
#             start_date,
#             end_date,
#         )

#         # Print a summary header
#         print(
#             f"\nRetrieved {len(klines)} klines for period from {start_date} to {end_date}.\n"
#         )

#         # Iterate over the returned candles and display basic info
#         for k in klines:
#             # k[0] = open time (ms), k[1] = open, k[2] = high, k[3] = low,
#             # k[4] = close, k[5] = volume
#             print(
#                 f"Time: {datetime.fromtimestamp(k[0]/1000)}, "
#                 f"O: {k[1]}, H: {k[2]}, L: {k[3]}, C: {k[4]}, V: {k[5]}"
#             )

#         return klines  # Return the raw klines data for further processing if needed
#     except Exception as e:
#         # Handle any errors during the data fetch or processing
#         print(f"Error fetching data: {e}")


# if __name__ == "__main__":
#     # Execute the main async function using asyncio.run()
#     asyncio.run(main())
