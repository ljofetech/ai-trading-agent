import os
import asyncio

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from client import BinanceAPI

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


async def get_current_candle(symbol: str, interval: str):
    binance = BinanceAPI(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
    await binance.connect()

    try:
        klines = await binance.client.futures_klines(
            symbol=symbol,
            interval=interval,
            limit=2,
        )

        if not klines:
            return None

        if len(klines) >= 2:
            candle = klines[-2]
        else:
            candle = klines[-1]

        result = {
            "open_time": datetime.fromtimestamp(candle[0] / 1000),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
            "close_time": datetime.fromtimestamp(candle[6] / 1000),
        }
        return result

    except Exception as e:
        print(f"Error when receiving futures candle: {e}")
        return None
    finally:
        await binance.disconnect()


async def main():
    candle = await get_current_candle("BTCUSDT", "5m")
    if candle:
        print(f"Open time: {candle['open_time']}")
        print(f"Open price: {candle['open']}")
        print(f"High: {candle['high']}")
        print(f"Low: {candle['low']}")
        print(f"Close: {candle['close']}")
        print(f"Volume: {candle['volume']}")
        print(f"Close time: {candle['close_time']}")
    else:
        print("Failed to retrieve candle.")


if __name__ == "__main__":
    asyncio.run(main())
