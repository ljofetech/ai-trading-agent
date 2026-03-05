class ExecutionAgent:

    @staticmethod
    def plan(state: dict, market_data: dict, risk_data: dict) -> dict:

        asset_in = market_data["asset_in"]
        asset_out = market_data["asset_out"]

        amount = ExecutionAgent.extract_amount(state["user_input"])
        slippage = ExecutionAgent.calculate_slippage(risk_data)

        return {
            "asset_in": asset_in,
            "asset_out": asset_out,
            "amount": amount,
            "max_slippage": slippage,
            "reasoning": "Based on liquidity and volatility analysis",
            "confidence": risk_data["confidence"],
        }

    @staticmethod
    def extract_amount(text: str) -> float:
        # в реальности — LLM extraction
        return 1000.0

    @staticmethod
    def calculate_slippage(risk_data: dict) -> float:
        if risk_data["risk_level"] == "low":
            return 0.005
        elif risk_data["risk_level"] == "medium":
            return 0.01
        return 0.02
