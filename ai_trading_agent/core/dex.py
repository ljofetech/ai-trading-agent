import requests


def get_market_data(token):

    response = requests.get(
        f"https://api.dex-trade.com/v1/public/ticker?pair={token}"
    ).json()

    data = response["data"]

    price = float(data["last"])
    high = float(data["high"])
    low = float(data["low"])
    volume = float(data["volume_24H"])

    result = {
        "token": data["pair"],
        "price": price,
        "volatility": (high - low) / price,
        "liquidity": volume * price,
    }

    return result
