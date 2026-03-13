from llmcouncil.client import LLMClient


class RiskAgent:

    @staticmethod
    def evaluate(state, market_data):

        analysis = LLMClient.generate(
            f"""
                Analyze trading risk.

                Market data:
                    {market_data}

                Return ONLY valid JSON:
                    {{
                    "risk_score": number,
                    "confidence": number,
                    "risk_level": "low | medium | high",
                    "reasoning": "text"
                    }}
            """
        )

        return analysis
