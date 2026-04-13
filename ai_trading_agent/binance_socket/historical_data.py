import os
import asyncio

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from client import BinanceAPI

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


async def get_historical_klines_range(
    symbol: str, interval: str, start_date: str, end_date: str
):
    binance = BinanceAPI(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=False)
    await binance.connect()

    try:
        klines = await binance.client.futures_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_date,
            end_str=end_date,
        )
        return klines
    finally:
        await binance.disconnect()


async def main():
    symbol = "BTCUSDT"
    interval = "15m"
    start_date = "1d ago UTC"
    end_date = "now UTC"

    try:
        klines = await get_historical_klines_range(
            symbol,
            interval,
            start_date,
            end_date,
        )

        print(
            f"\nRetrieved {len(klines)} klines for period from {start_date} to {end_date}.\n"
        )
        for k in klines:
            print(
                f"Time: {datetime.fromtimestamp(k[0]/1000)}, O: {k[1]}, H: {k[2]}, L: {k[3]}, C: {k[4]}, V: {k[5]}"
            )
    except Exception as e:
        print(f"Error fetching data: {e}")


if __name__ == "__main__":
    asyncio.run(main())
