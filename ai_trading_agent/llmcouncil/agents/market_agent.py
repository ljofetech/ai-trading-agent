import requests


class MarketAgent:

    @staticmethod
    def analyze(state: dict) -> dict:
        """
        Анализирует рынок и возвращает структурированные метрики.
        """

        user_input = state["user_input"]

        # 1. Извлечение токенов (в реальном проекте — LLM parsing)
        asset_in = "USDC"
        asset_out = "ETH"

        # 2. Получение рыночных данных
        price = MarketAgent.get_price(asset_out)
        liquidity = MarketAgent.get_liquidity(asset_out)
        volatility = MarketAgent.get_volatility(asset_out)

        return {
            "asset_in": asset_in,
            "asset_out": asset_out,
            "price": price,
            "liquidity": liquidity,
            "volatility": volatility,
        }

    @staticmethod
    def get_price(symbol: str) -> float:
        # заглушка
        return 3200.0

    @staticmethod
    def get_liquidity(symbol: str) -> float:
        return 15_000_000

    @staticmethod
    def get_volatility(symbol: str) -> float:
        return 0.032
