from llmcouncil.client import LLMClient


class RiskAgent:

    @staticmethod
    def evaluate(state, market_data):

        analysis = LLMClient.generate_json(
            f"""
                Analyze trading risk.

                Market data:
                    {market_data}

                Return JSON:

                    {{
                    "risk_score": number,
                    "confidence": number,
                    "risk_level": "low | medium | high",
                    "reasoning": "text"
                    }}
            """
        )

        return analysis
