from llmcouncil.client import LLMClient


class ExecutionAgent:

    @staticmethod
    def plan(state: dict, market_data: dict, risk_data: dict):

        response = LLMClient.generate(
            f"""
                1. Create trade execution plan.
                2. And in "reasoning", speak easily and clearly.

                User message:
                    {state["user_input"]}

                Market data:
                    {market_data}

                Risk data:
                    {risk_data}

                Return ONLY valid JSON:
                    {{
                    "asset_in": "...",
                    "asset_out": "...",
                    "amount": number,
                    "max_slippage": number,
                    "confidence": number,
                    "reasoning": "text"
                    }}
            """
        )

        return response
