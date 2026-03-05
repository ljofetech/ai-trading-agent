import requests


def get_market_data(token):

    # здесь можно подключить любую API
    # например dex-trade или coingecko

    return {"token": token, "price": 2400, "volatility": 0.12, "liquidity": 8000000}
