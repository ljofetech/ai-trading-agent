from datetime import datetime, timedelta

from llmcouncil.client import LLMClient
from binance_socket.historical_data import get_historical_klines_range
from Kronos.examples.test import KronosForecaster


class MarketAgent:

    @staticmethod
    def analyze(state: dict):
        user_input = state["user_input"]

        extraction = LLMClient.generate(f"""
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
            """)

        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        asset_in = extraction.get("asset_in") or "BTC"
        asset_out = extraction.get("asset_out") or "USDT"
        timeframe = extraction.get("timeframe") or "15m"
        start_date = extraction.get("start_date") or today.isoformat()
        end_date = extraction.get("end_date") or tomorrow.isoformat()

        # Convert ISO strings to datetime objects
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)

        # Calculate difference in hours
        hours = round((end_dt - start_dt).total_seconds() / 3600)

        symbol = asset_in + asset_out

        history = get_historical_klines_range(
            symbol,
            timeframe,
            start_date,
            end_date,
        )

        forecaster = KronosForecaster(
            symbol=symbol,
            interval=timeframe,
            limit=500,
            pred_len=50,
            lookback=400,
            forecast_hours=hours,
        )
        dataframe, pred_df = forecaster.predict()

        return {
            "prediction": pred_df.reset_index().to_dict(orient="records"),
            "history": history,
        }
