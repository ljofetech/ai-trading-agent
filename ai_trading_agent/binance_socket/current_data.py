import os
import asyncio

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from client import BinanceAPI

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


async def stream_futures_candle(symbol: str, interval: str):
    binance = BinanceAPI(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=False)
    await binance.connect()

    try:
        stream_name = f"{symbol.lower()}@kline_{interval}"

        socket = binance.socket_manager.futures_multiplex_socket([stream_name])

        async with socket as stream:
            while True:
                msg = await stream.recv()

                kline = msg["data"]["k"]

                candle = {
                    "open_time": datetime.fromtimestamp(kline["t"] / 1000),
                    "open": float(kline["o"]),
                    "high": float(kline["h"]),
                    "low": float(kline["l"]),
                    "close": float(kline["c"]),
                    "volume": float(kline["v"]),
                    "close_time": datetime.fromtimestamp(kline["T"] / 1000),
                    "closed": kline["x"],
                }

                print(candle)

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        await binance.disconnect()


if __name__ == "__main__":
    asyncio.run(stream_futures_candle("BTCUSDT", "15m"))
