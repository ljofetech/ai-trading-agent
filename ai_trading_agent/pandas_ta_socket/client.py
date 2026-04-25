import os
import pandas as pd
import ccxt
import pandas_ta as ta

# For datetime handling and timezone conversion
from datetime import datetime
from tzlocal import get_localzone

# For loading environment variables from .env file
from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()

# Retrieve Binance API credentials from environment variables
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
        """
        Initialize the analyzer with trading pair, date range, timeframe, and desired indicators.

        :param symbol: Trading pair symbol (e.g., 'BTCUSDT')
        :param start_date: Start date in 'YYYY-MM-DD' format
        :param end_date: End date in 'YYYY-MM-DD' format
        :param timeframe: Candle interval (e.g., '1h', '15m')
        :param indicators: List of indicator names to compute (e.g., ['rsi', 'bbands'])
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        # Default indicators if none provided
        self.indicators = indicators if indicators else ["rsi", "bbands", "ema"]
        self.data = None  # Will hold the OHLCV DataFrame
        # Configure Binance USDⓈ-M Futures exchange connection
        self.exchange = ccxt.binanceusdm(
            {
                "apiKey": BINANCE_API_KEY,
                "secret": BINANCE_API_SECRET,
                "enableRateLimit": True,  # Respect rate limits
                "testnet": False,  # Use live mainnet
                "options": {
                    "fetchCurrencies": False,  # Skip fetching currencies to speed up
                },
            }
        )
        # Track which indicator columns were added (for reporting)
        self.added_indicators_info = []

    def _fetch_data(self) -> pd.DataFrame:
        """
        Fetch historical OHLCV data from Binance for the given symbol and date range.

        :return: DataFrame with columns: timestamp, open, high, low, close, volume
        """
        # Load market info to ensure symbol is valid
        self.exchange.load_markets()
        # Convert start and end dates to timestamps (milliseconds since epoch)
        since = self.exchange.parse8601(f"{self.start_date}T00:00:00Z")
        end_timestamp = self.exchange.parse8601(f"{self.end_date}T23:59:59Z")
        all_ohlcv = []  # Accumulate all candles

        # Paginate through historical data in chunks of up to 1000 candles
        while since < end_timestamp:
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=self.symbol, timeframe=self.timeframe, since=since, limit=1000
            )
            if not ohlcv:
                break  # No more data available
            all_ohlcv.extend(ohlcv)
            # Move 'since' to the next timestamp after the last candle received
            since = ohlcv[-1][0] + 1

        # Convert the list of lists into a pandas DataFrame
        df = pd.DataFrame(
            all_ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        # Convert timestamp (ms) to datetime (UTC)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        # Filter to the exact requested date range (inclusive)
        mask = (df.index >= self.start_date) & (df.index <= self.end_date)
        return df.loc[mask].copy()

    def _add_indicators(self) -> None:
        """
        Add technical indicators to the data using pandas_ta.
        Updates self.data in-place and records added column names.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Mapping from indicator name to (function, keyword arguments)
        # pandas_ta functions are called with append=True to add columns directly to self.data
        indicator_config = {
            "rsi": (self.data.ta.rsi, {"length": 14}),  # Relative Strength Index
            "bbands": (
                self.data.ta.bbands,
                {"length": 20, "std": 2},
            ),  # Bollinger Bands
            "ema": (self.data.ta.ema, {"length": 20}),  # Exponential Moving Average
        }

        cols_before = set(self.data.columns)  # Snapshot of existing columns

        for ind in self.indicators:
            ind_lower = ind.lower()
            if ind_lower in indicator_config:
                func, kwargs = indicator_config[ind_lower]
                # Call the indicator function, appending new columns to the DataFrame
                func(append=True, **kwargs)
                # Detect which columns were added by comparing with previous snapshot
                cols_after = set(self.data.columns)
                new_cols = list(cols_after - cols_before)
                if new_cols:
                    self.added_indicators_info.append(
                        {"indicator": ind.upper(), "columns": new_cols}
                    )
                    print(f"✅ Indicator added: {ind.upper()} -> {new_cols}")
                cols_before = cols_after  # Update snapshot for next indicator
            else:
                print(f"⚠️ Warning: Indicator '{ind}' is not supported.")

    def load_data(self) -> pd.DataFrame:
        """
        Fetch historical data and add technical indicators.

        :return: DataFrame with OHLCV data and indicator columns
        """
        print(
            f"📥 Loading data for {self.symbol} from {self.start_date} to {self.end_date} and timeframe {self.timeframe}..."
        )
        self.data = self._fetch_data()
        if self.data.empty:
            print("❌ No data found. Check ticker and dates.")
            return self.data

        print(f"✅ Loaded {len(self.data)} candles.")
        self._add_indicators()  # Compute and append indicators
        return self.data

    def get_data(self, local_time: bool = False) -> pd.DataFrame:
        """
        Return the processed DataFrame, optionally converting index to local timezone.

        :param local_time: If True, convert UTC index to system's local timezone
        :return: Copy of the data DataFrame
        """
        if self.data is None:
            self.load_data()  # Lazy loading
        df = self.data.copy()
        if local_time:
            df.index = df.index.tz_convert(get_localzone())
        return df


# if __name__ == "__main__":
#     # --- Example usage ---
#     # Create an instance of the analyzer for BTC/USDT, one day of 15-minute candles
#     analyzer = CryptoAnalyzer(
#         symbol="BTCUSDT",
#         start_date="2026-04-20",
#         end_date="2026-04-21",
#         timeframe="15m",
#         indicators=["rsi", "bbands", "ema"],
#     )

#     # Load data and get the enriched DataFrame (local timezone for readability)
#     df = analyzer.get_data(local_time=True)

#     # Display all column names to verify indicators are present
#     print("\n📊 DataFrame columns:")
#     print(df.columns.tolist())

#     # Show the last few rows, focusing on price, volume, and computed indicators
#     print("\n📈 Last rows with indicators:")
#     display_cols = [
#         "open",
#         "high",
#         "low",
#         "close",
#         "volume",
#         "RSI_14",
#         "EMA_20",
#         "BBL_20_2.0",
#         "BBM_20_2.0",
#         "BBU_20_2.0",
#     ]
#     available_cols = [col for col in display_cols if col in df.columns]
#     print(df[available_cols].tail())

#     # Save the complete DataFrame to a CSV file (creates 'analysis' directory if needed)
#     output_file = f"analysis/btc_usdt_{analyzer.start_date}_{analyzer.end_date}_with_indicators.csv"
#     df.to_csv(output_file)
#     print(f"\n💾 Data saved to '{output_file}'")

#     # Quick verification: read back the CSV and show its columns
#     check_df = pd.read_csv(output_file, index_col=0)
#     print(f"📁 Saved file columns: {check_df.columns.tolist()}")
