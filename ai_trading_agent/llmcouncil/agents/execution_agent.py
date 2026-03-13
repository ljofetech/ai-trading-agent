from llmcouncil.client import LLMClient


class ExecutionAgent:

    @staticmethod
    def plan(state, market_data, risk_data):

        response = LLMClient.generate(
            f"""
                Create trade execution plan.

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
