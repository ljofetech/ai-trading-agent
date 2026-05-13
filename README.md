# Required

## Files for project

```json
// The `\trading_agent\.env` file is a configuration file for the project located in the
// `trading_agent` directory. It typically contains settings such as `SECRET_KEY`, `DEBUG`,
// `ALLOWED_HOSTS`, and `GEMINI_API_KEY` with their corresponding values. These settings are crucial
// for the project's functionality and may include sensitive information like API keys.
\trading_agent\.env

// You can run this code from the 'trading_agent' directory using: py secret_key.py
// This will generate a secure Django SECRET_KEY for use in your project settings.

// The lines `SECRET_KEY = string`, `DEBUG = int`, and `ALLOWED_HOSTS = string` are configuration
// settings in a `.env` file for a project. Here's what each of these settings typically represents:
SECRET_KEY = string
DEBUG = int
ALLOWED_HOSTS = string

// `AI_API_KEY = string` is a configuration setting in the `.env` file for the project. This
// setting typically represents the API key required for accessing the AI API. The value assigned
// to `AI_API_KEY` should be the actual API key provided by AI for authentication and
// authorization purposes when interacting with their API services.
AI_API_KEY = string

// The lines `BINANCE_API_KEY = string` and `BINANCE_API_SECRET = string` are configuration settings in
// a `.env` file for a project that involve storing sensitive information related to the Binance API.
BINANCE_API_KEY = string
BINANCE_API_SECRET = string

// `TIME_ZONE = "Asia/Nicosia"` and `USE_TZ = True` are settings in a configuration file (`.env` file)
// for a project.
TIME_ZONE = "Asia/Nicosia"
USE_TZ = True

// The values `T=0.5`, `top_p=0.8`, and `sample_count=1` are configuration settings used in the context
// of forecasting scenarios within the Kronos system. Here's what each of these settings represents:
T=0.5
top_p=0.8
sample_count=1

// The code snippet `symbol="BTCUSDT" interval="15m" forecast_hours=5` is defining parameters related
// to trading and forecasting within the project. Here's what each parameter represents:
symbol="BTCUSDT"
interval="15m"
forecast_hours=5
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

// The list of packages is related to the dependencies being installed for a project. When
// you run the command `pip install -r .\requirements.txt`, it reads the `requirements.txt` file which
// contains a list of all the Python packages and libraries required for the project to function
// properly.
Installing collected packages: pytz, mpmath, zstandard, xxhash, websockets, wcwidth, vine, uuid-utils, urllib3, uritemplate, tzdata, typing-extensions, tenacity, sympy, sqlparse, six, setuptools, safetensors, rpds-py, regex, redis, PyYAML, python-dotenv, pyparsing, pycryptodome, pycparser, propcache, pillow, packaging, ormsgpack, orjson, numpy, networkx, multidict, MarkupSafe, llvmlite, kiwisolver, jsonpointer, inflection, idna, h11, fsspec, frozenlist, fonttools, filelock, einops, cycler, colorama, coincurve, charset_normalizer, certifi, billiard, attrs, asgiref, annotated-types, aiohappyeyeballs, yarl, tzlocal, typing-inspection, tqdm, requests, referencing, python-dateutil, pydantic-core, prompt-toolkit, numba, langchain-protocol, jsonpatch, jinja2, httpcore, django, contourpy, click, cffi, anyio, amqp, aiosignal, torch, requests-toolbelt, pydantic, pycares, pandas, matplotlib, kombu, jsonschema-specifications, huggingface_hub, httpx, djangorestframework, dateparser, cryptography, click-repl, click-plugins, click-didyoumean, aiohttp, python-binance, pandas-ta, langsmith, langgraph-sdk, jsonschema, celery, aiodns, langchain-core, drf-spectacular, ccxt, langgraph-checkpoint, langgraph-prebuilt, langgraph
```

### Kronos

```json
# Stable forecast (minimum noise)
T=0.5,  # Low temperature → almost deterministic forecast (less noise)
top_p=0.8,  # We take only the most probable options → smoothed result
sample_count=1,  # One scenario → simple, without variability

# Balanced (default recommended)
T=0.8, # Balance between stability and variability
top_p=0.9, # Likely scenarios are taken into account, but not only the most severe ones
sample_count=3, # Several scenarios → can be averaged

# Aggressive / “market chaos”
T=1.2, # High temperature → more randomness
top_p=0.95, # Almost the entire spectrum of probabilities → chaos
sample_count=5, # Several scenarios → different possible futures

# Uncertainty Analysis (very useful)
T=0.9, # a little randomness
top_p=0.9, # normal probability range
sample_count=10, # many scenarios

# Short accurate forecast (scalping)
T=0.6, # less noise → more precisely short-term
top_p=0.85, # focus on probable movements
sample_count=1,

# | Parameter      | What it does                         | Lower value                 | Higher value                |
# | -------------- | ------------------------------------ | --------------------------- | --------------------------- |
# | `T`            | randomness (temperature)             | more stable, deterministic  | more chaotic, unpredictable |
# | `top_p`        | probability range (nucleus sampling) | conservative, safer choices | more diverse possibilities  |
# | `sample_count` | number of scenarios                  | single forecast path        | multiple possible futures   |
# | `pred_len`     | forecast length                      | short-term prediction       | long-term prediction        |

```

### TEST OBJECT

```json
{
"conversation_id": "0",
"message": "I want to trade BTC for USDT using a 15m timeframe, starting from 2026-05-13 and ending at 2026-05-14"
}
```

### API KEY

<https://www.binance.com/en/support/faq/detail/360002502072>

### API PACKAGES

<https://python-binance.readthedocs.io/en/latest/>

<https://sammchardy.github.io/async-binance-basics/>

<https://github.com/sammchardy/python-binance/tree/master/examples>

### PLAN PACKAGES

<https://www.pandas-ta.dev/getting-started/installation/>

<https://www.pandas-ta.dev/api/>

<https://huggingface.co/NeoQuasar/Kronos-base>

<https://openrouter.ai/>

### PROJECT INFO

<https://docs.google.com/document/d/1gX6cKdLb4sdMJgOvAT85z0pJ4ZbtNm_yZyx9FnvUpsM/edit?usp=sharing>
