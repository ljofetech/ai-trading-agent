from llmcouncil.client import LLMClient


class RiskAgent:

    @staticmethod
    def evaluate(market_data: dict):

        analysis = LLMClient.generate(
            f"""
                1. Analyze trading risk.

                Market data:
                    {market_data}

                Return ONLY valid JSON:
                    {{
                    "risk_score": number,
                    "confidence": number,
                    "risk_level": "low | medium | high"
                    }}
            """
        )

        return analysis
