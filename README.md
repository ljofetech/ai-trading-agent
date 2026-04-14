# Required

## Files for project

```json
// The `\trading_agent\.env` file is a configuration file for the project located in the
// `trading_agent` directory. It typically contains settings such as `SECRET_KEY`, `DEBUG`,
// `ALLOWED_HOSTS`, and `GEMINI_API_KEY` with their corresponding values. These settings are crucial
// for the project's functionality and may include sensitive information like API keys.
\trading_agent\.env

// The lines `SECRET_KEY = string`, `DEBUG = int`, and `ALLOWED_HOSTS = string` are configuration
// settings in a `.env` file for a project. Here's what each of these settings typically represents:
SECRET_KEY = string
DEBUG = int
ALLOWED_HOSTS = string

// `GEMINI_API_KEY = string` is a configuration setting in the `.env` file for the project. This
// setting typically represents the API key required for accessing the Gemini API. The value assigned
// to `GEMINI_API_KEY` should be the actual API key provided by Gemini for authentication and
// authorization purposes when interacting with their API services.
GEMINI_API_KEY = string
```

## Requirments

```json
// This command `\trading_agent> py -m venv venv` is creating a new virtual environment named `venv`
// for the project located in the `trading_agent` directory using the Python interpreter.
\trading_agent> py -m venv venv

// The command `\trading_agent> venv/scripts/activate` is activating the virtual environment named
// `venv` that was created in the `trading_agent` directory. This command sets up the environment
// variables and paths so that when you run Python or install packages, it will be isolated within the
// virtual environment rather than affecting the system-wide Python installation.
\trading_agent> venv/scripts/activate

// `\trading_agent> pip install -r .\requirements.txt` is a command that is used to install all the
// required dependencies listed in the `requirements.txt` file for the project located in the
// `trading_agent` directory. The `-r` flag specifies that the dependencies should be installed from
// the specified requirements file. This command ensures that all the necessary Python packages and
// libraries are installed in the virtual environment to run the project successfully.
\trading_agent> pip install -r .\requirements.txt
```

### API KEY

<https://www.binance.com/en/support/faq/detail/360002502072>

### API PACKAGE

<https://python-binance.readthedocs.io/en/latest/>

<https://sammchardy.github.io/async-binance-basics/>

<https://github.com/sammchardy/python-binance/tree/master/examples>


<https://www.pandas-ta.dev/getting-started/installation/>

<https://www.pandas-ta.dev/api/>

### PROJECT INFO

<https://docs.google.com/document/d/1gX6cKdLb4sdMJgOvAT85z0pJ4ZbtNm_yZyx9FnvUpsM/edit?usp=sharing>

---

### 📊 Breakdown of the Data Structure

The `listen_kline` function returns a `JSON` object containing two main sections: general event information (`e`, `E`, `s`) and a nested `k` object with the candlestick data itself. Inside the `k` object are the fields `t`, `T`, `s`, `i`, as well as important trading indicators `o`, `c`, `h`, `l`, `v`.

* **General Event Fields:**
  * `e` (event type): The type of event. The value `kline` confirms that this is candlestick data.
  * `E` (event time): The event time in milliseconds (`Unix Timestamp`).
  * `s` (symbol): The trading pair. In your case, `BNBBTC`.
* **Candlestick Data (`k` object):**
  * `t` (kline start time): The start time of the candlestick in milliseconds.
  * `T` (kline close time): The close time of the candlestick.
  * `s` (symbol): Duplicates the trading pair for convenience.
  * `i` (interval): The candlestick interval. `1m` means one minute.
  * `o` (open price): Opening price (`0.00831400`).
  * `c` (close price): Closing price. In your example, it is equal to the opening price.
  * `h` (high price): Maximum price for the period.
  * `l` (low price): Minimum price for the period.
  * `v` (base asset volume): Trading volume in the base asset (BNB).
  * `n` (number of trades): The number of trades executed.
  * `x` (is closed): The status of the candlestick. `True` means it is closed (final).
  * `q` (quote asset volume): Trading volume in the quote asset (BTC).
  * `V` (taker buy base volume): Volume of market buy orders in the base asset.
  * `Q` (taker buy quote volume): Volume of market buy orders in the quote asset.
  * `B` (ignore): An ignored parameter.
