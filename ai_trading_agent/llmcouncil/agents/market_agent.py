from core.dex import get_market_data


class MarketAgent:

    @staticmethod
    def analyze(state: dict) -> dict:
        """
        Анализирует рынок и возвращает структурированные метрики.
        """

        user_input = state.get("user_input", "")

        assets = MarketAgent.parse_user_input(user_input)
        asset_in = assets["asset_in"].upper()
        asset_out = assets["asset_out"].upper()

        pair = f"{asset_in}{asset_out}"  # пример: BTCUSDT

        ticker_data = get_market_data(pair)

        price = float(ticker_data.get("price", 0))
        liquidity = float(ticker_data.get("volatility", 0))
        volatility = float(ticker_data.get("liquidity", 0))

        return {
            "asset_in": asset_in,
            "asset_out": asset_out,
            "price": price,
            "liquidity": liquidity,
            "volatility": volatility,
        }

    @staticmethod
    def parse_user_input(user_input: str) -> dict:
        """
        Простое извлечение валют из строки.
        Можно заменить на LLM для сложных сообщений.
        """
        tokens = user_input.upper().split()
        if len(tokens) >= 2:
            return {"asset_in": tokens[0], "asset_out": tokens[1]}
        # fallback
        return {"asset_in": "BTC", "asset_out": "USDT"}
