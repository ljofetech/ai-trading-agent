import requests


def get_market_data(token):

    response = requests.get(
        f"https://api.dex-trade.com/v1/public/ticker?pair={token}",
        timeout=5,
    )

    response.raise_for_status()
    payload = response.json()

    data = payload["data"]

    price = float(data.get("last", 0))
    high = float(data.get("high", 0))
    low = float(data.get("low", 0))
    volume = float(data.get("volume_24H", 0))

    result = {
        "token": data.get("pair"),
        "price": price,
        "volatility": (high - low) / price if price else 0,
        "liquidity": volume * price,
    }

    return result
