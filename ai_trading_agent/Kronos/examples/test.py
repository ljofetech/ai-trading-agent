import sys
import os
import requests
import pandas as pd

# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

# Add parent directory to Python path to allow local module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import Kronos, KronosTokenizer, KronosPredictor


class KronosForecaster:
    """
    Handles:
    - Fetching market data from Binance
    - Loading Kronos model
    - Preparing data
    - Running predictions
    - (Optional) plotting results
    """

    def __init__(
        self,
        symbol,
        interval,
        limit,
        pred_len,
        lookback,
        forecast_hours,
    ):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.lookback = lookback

        if forecast_hours is not None:
            # Convert interval string (e.g. "15m", "1h", "4h", "1d") into minutes
            # pd.Timedelta doesn't like "m" suffix, so replace "m" → "min"
            freq_str = self.interval.replace("m", "min")
            try:
                minutes_per_candle = pd.Timedelta(freq_str).total_seconds() / 60
            except ValueError:
                raise ValueError(
                    f"Unsupported interval format: {self.interval}. "
                    "Use something like '1m','5m','15m','1h','4h','1d'."
                )

            steps = int(round(forecast_hours * 60 / minutes_per_candle))
            if steps < 1:
                raise ValueError(
                    f"forecast_hours={forecast_hours} gives zero steps "
                    f"with interval {self.interval}. Increase the horizon."
                )
            self.pred_len = steps
            print(
                f"🔮 Forecast horizon: {forecast_hours}h → {self.pred_len} steps "
                f"(interval: {self.interval})"
            )
        else:
            self.pred_len = pred_len
        # -----------------------------------------------------------------

        # Load model once (important for performance)
        self.tokenizer = KronosTokenizer.from_pretrained(
            "NeoQuasar/Kronos-Tokenizer-base"
        )
        self.model = Kronos.from_pretrained("NeoQuasar/Kronos-small")
        self.predictor = KronosPredictor(self.model, self.tokenizer, max_context=512)

    # ================================
    # Fetch Binance data
    # ================================
    def fetch_data(self):
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "limit": self.limit,
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(
            data,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "qav",
                "trades",
                "taker_base_vol",
                "taker_quote_vol",
                "ignore",
            ],
        )

        # Convert types
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)

        df["timestamp"] = pd.to_datetime(
            df["open_time"], unit="ms", utc=settings.USE_TZ
        ).dt.tz_convert(settings.TIME_ZONE)

        return df

    # ================================
    # Prepare model input
    # ================================
    def prepare_data(self, df):
        # Use most recent lookback window
        x_df = df[["open", "high", "low", "close", "volume"]].iloc[-self.lookback :]
        x_timestamp = df["timestamp"].iloc[-self.lookback :]

        # Use latest available timestamp
        last_time = df["timestamp"].iloc[-1]

        # ----- NEW: use the actual candle interval for future timestamps -----
        # Replace "m" → "min" so pd.date_range understands it
        freq_for_range = self.interval.replace("m", "min")

        # Create the future time axis with the correct frequency and number of steps
        future_times = pd.date_range(
            start=last_time,
            periods=self.pred_len + 1,
            freq=freq_for_range,
            tz=settings.TIME_ZONE,
        )[1:]
        return x_df, x_timestamp, future_times

    # ================================
    # Run prediction
    # ================================
    def predict(self):
        df = self.fetch_data()
        x_df, x_timestamp, future_times = self.prepare_data(df)

        pred_df = self.predictor.predict(
            df=x_df,  # Historical OHLCV data
            x_timestamp=x_timestamp,  # Time for a story
            y_timestamp=pd.Series(future_times),  # Future time grid
            pred_len=self.pred_len,  # Forecast length (number of steps)
            T=float(os.getenv("T")),
            top_p=float(os.getenv("top_p")),
            sample_count=int(os.getenv("sample_count")),
        )

        return df, pred_df

    # ================================
    # Plot with exact time & price for every forecast step
    # ================================
    # def plot(self, df, pred_df, date_format="%Y-%m-%d %H:%M"):
    #     fig, ax = plt.subplots(figsize=(16, 8))

    #     # History line
    #     ax.plot(
    #         df["timestamp"][: self.lookback],
    #         df["close"][: self.lookback],
    #         linewidth=1.5,
    #         label="History",
    #         color="dodgerblue",
    #     )

    #     # Forecast line with markers
    #     ax.plot(
    #         pred_df.index,
    #         pred_df["close"],
    #         linewidth=1.5,
    #         marker="o",
    #         markersize=5,
    #         linestyle="--",
    #         label="Forecast",
    #         color="crimson",
    #     )

    #     # ---- EXACT TIME TICKS FOR EVERY FORECAST STEP ----
    #     # Use pred_df.index as the tick positions (only these will be labeled)
    #     ax.set_xticks(pred_df.index)

    #     # Format: day + hour:minute (e.g., "5 14:35"). If all points are same day, we could use only "%H:%M",
    #     # but this is safer for multi‑day forecasts.
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

    #     # Rotate for readability
    #     plt.setp(ax.get_xticklabels(), rotation=60, ha="right", fontsize=8)

    #     # ---- ANNOTATE EACH FORECAST POINT WITH ITS PRICE ----
    #     for x, y in zip(pred_df.index, pred_df["close"]):
    #         ax.annotate(
    #             f"{y:.2f}",  # price formatted
    #             (x, y),
    #             textcoords="offset points",
    #             xytext=(0, 12),  # slightly above the marker
    #             ha="center",
    #             fontsize=7,
    #             color="darkred",
    #             bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
    #         )

    #     # ---- GRID MATCHING FORECAST STEPS ----
    #     ax.grid(
    #         True, which="major", axis="both", linestyle="-", linewidth=0.5, alpha=0.7
    #     )
    #     # Turn off minor grid (it would be too dense)
    #     ax.grid(False, which="minor")

    #     # ---- PRICE AXIS ----
    #     ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.2f}"))
    #     ax.set_ylabel("Price (USDT)", fontsize=10)

    #     ax.set_xlabel("Time (UTC)", fontsize=10)
    #     ax.set_title(
    #         f"{self.symbol} Forecast – step={self.pred_len} points", fontsize=14
    #     )
    #     ax.legend(loc="best")

    #     plt.tight_layout()
    #     plt.show()


# forecaster = KronosForecaster(
#     symbol="BTCUSDT",
#     interval="15m",
#     limit=500,
#     lookback=400,
#     forecast_hours=2
# )
# df, pred_df = forecaster.predict()
# forecaster.plot(df, pred_df)

# forecaster_24h = KronosForecaster(
#     symbol="ETHUSDT",
#     interval="1h",
#     forecast_hours=24
# )
