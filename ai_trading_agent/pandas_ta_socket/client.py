import os
import pandas as pd
import ccxt
import pandas_ta as ta

from datetime import datetime
from tzlocal import get_localzone

from dotenv import load_dotenv

load_dotenv()


BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


class CryptoAnalyzer:
    """
    Class for loading historical data from a cryptocurrency exchange and adding technical indicators.
    """

    def __init__(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        timeframe: str,
        indicators: list,
    ):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.indicators = indicators if indicators else ["rsi", "bbands", "ema"]
        self.data = None
        self.exchange = ccxt.binanceusdm(
            {
                "apiKey": BINANCE_API_KEY,
                "secret": BINANCE_API_SECRET,
                "enableRateLimit": True,
                "testnet": False,
                "options": {
                    "fetchCurrencies": False,
                },
            }
        )
        self.added_indicators_info = []

    def _fetch_data(self) -> pd.DataFrame:
        self.exchange.load_markets()
        since = self.exchange.parse8601(f"{self.start_date}T00:00:00Z")
        end_timestamp = self.exchange.parse8601(f"{self.end_date}T23:59:59Z")
        all_ohlcv = []

        while since < end_timestamp:
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=self.symbol, timeframe=self.timeframe, since=since, limit=1000
            )
            if not ohlcv:
                break
            all_ohlcv.extend(ohlcv)
            since = ohlcv[-1][0] + 1

        df = pd.DataFrame(
            all_ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        mask = (df.index >= self.start_date) & (df.index <= self.end_date)
        return df.loc[mask].copy()

    def _add_indicators(self) -> None:
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Dictionary mapping indicator names to (method, kwargs)
        indicator_config = {
            "rsi": (self.data.ta.rsi, {"length": 14}),
            "bbands": (self.data.ta.bbands, {"length": 20, "std": 2}),
            "ema": (self.data.ta.ema, {"length": 20}),
        }

        cols_before = set(self.data.columns)

        for ind in self.indicators:
            ind_lower = ind.lower()
            if ind_lower in indicator_config:
                func, kwargs = indicator_config[ind_lower]
                # Call indicator function with append=True
                func(append=True, **kwargs)
                # Detect newly added columns
                cols_after = set(self.data.columns)
                new_cols = list(cols_after - cols_before)
                if new_cols:
                    self.added_indicators_info.append(
                        {"indicator": ind.upper(), "columns": new_cols}
                    )
                    print(f"✅ Indicator added: {ind.upper()} -> {new_cols}")
                cols_before = cols_after
            else:
                print(f"⚠️ Warning: Indicator '{ind}' is not supported.")

    def load_data(self) -> pd.DataFrame:
        print(
            f"📥 Loading data for {self.symbol} from {self.start_date} to {self.end_date} and timeframe {self.timeframe}..."
        )
        self.data = self._fetch_data()
        if self.data.empty:
            print("❌ No data found. Check ticker and dates.")
            return self.data

        print(f"✅ Loaded {len(self.data)} candles.")
        self._add_indicators()
        return self.data

    def get_data(self, local_time: bool = False) -> pd.DataFrame:
        if self.data is None:
            self.load_data()
        df = self.data.copy()
        if local_time:
            df.index = df.index.tz_convert(get_localzone())
        return df


if __name__ == "__main__":
    # Create analyzer
    analyzer = CryptoAnalyzer(
        symbol="BTCUSDT",
        start_date="2026-04-15",
        end_date="2026-04-17",
        timeframe="15m",
        indicators=["rsi", "bbands", "ema"],
    )

    # Get enriched DataFrame
    df = analyzer.get_data(local_time=True)

    # Display columns to confirm presence of indicators
    print("\n📊 DataFrame columns:")
    print(df.columns.tolist())

    # Show tail with selected columns including indicators
    print("\n📈 Last rows with indicators:")
    display_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "RSI_14",
        "EMA_20",
        "BBL_20_2.0",
        "BBM_20_2.0",
        "BBU_20_2.0",
    ]
    available_cols = [col for col in display_cols if col in df.columns]
    print(df[available_cols].tail())

    # Save to CSV (ensure it contains all columns)
    output_file = f"analysis/btc_usdt_{analyzer.start_date}_{analyzer.end_date}_with_indicators.csv"
    df.to_csv(output_file)
    print(f"\n💾 Data saved to '{output_file}'")

    # Verify saved file
    check_df = pd.read_csv(output_file, index_col=0)
    print(f"📁 Saved file columns: {check_df.columns.tolist()}")
