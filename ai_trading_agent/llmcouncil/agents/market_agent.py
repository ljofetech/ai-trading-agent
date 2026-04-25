from datetime import datetime, timedelta

from llmcouncil.client import LLMClient
from binance_socket.current_data import get_current_futures_candle
from binance_socket.historical_data import get_historical_klines_range
from pandas_ta_socket.client import CryptoAnalyzer


class MarketAgent:

    @staticmethod
    def analyze(state: dict):
        user_input = state["user_input"]

        extraction = LLMClient.generate(
            f"""
            Extract trading pair, timeframe, start_date, and end_date from the message.
            - trading pair: asset_in and asset_out (e.g., BTC, USD)
            - timeframe: time like 1s, 15m, 1h, 4h, 1d, etc.
            - start_date, end_date: dates if present.

            Message: {user_input}

            Return ONLY valid JSON:
            {{
                "asset_in": "...",
                "asset_out": "...",
                "timeframe": "...",
                "start_date": "...",
                "end_date": "..."
            }}
            """
        )

        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        asset_in = extraction.get("asset_in") or "BTC"
        asset_out = extraction.get("asset_out") or "USDT"
        timeframe = extraction.get("timeframe") or "15m"
        start_date = extraction.get("start_date") or today.isoformat()
        end_date = extraction.get("end_date") or tomorrow.isoformat()

        symbol = asset_in + asset_out

        current_candle = get_current_futures_candle(
            symbol,
            timeframe,
        )
        history = get_historical_klines_range(
            symbol,
            timeframe,
            start_date,
            end_date,
        )
        analyzer = CryptoAnalyzer(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            timeframe=timeframe,
            indicators=["rsi", "bbands", "ema"],
        )
        df = analyzer.get_data(local_time=True)

        # Convert DataFrame to a NumPy array
        #data_array = df.to_numpy()  # or df.values (older pandas versions)

        # Or convert to a Python list of lists
        data_list = df.values.tolist()

        analysis = LLMClient.generate(
            f"""
            """
        )

        return {current_candle, history, data_list}
