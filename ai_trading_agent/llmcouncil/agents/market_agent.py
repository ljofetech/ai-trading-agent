from llmcouncil.client import LLMClient
from core.dex import get_market_data


class MarketAgent:

    @staticmethod
    def analyze(state: dict):

        user_input = state["user_input"]

        extraction = LLMClient.generate(
            f"""
                1. Extract trading pair from message.

                Message:
                    {user_input}

                Return ONLY valid JSON:
                    {{
                    "asset_in": "...",
                    "asset_out": "..."
                    }}
            """
        )

        asset_in = extraction["asset_in"]
        asset_out = extraction["asset_out"]

        pair = f"{asset_in}{asset_out}"

        ticker_data = get_market_data(pair)

        return {
            "asset_in": asset_in,
            "asset_out": asset_out,
            "price": float(ticker_data.get("price", 0)),
            "liquidity": float(ticker_data.get("liquidity", 0)),
            "volatility": float(ticker_data.get("volatility", 0)),
        }
