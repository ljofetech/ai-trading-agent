class RiskAgent:

    @staticmethod
    def evaluate(state: dict, market_data: dict) -> dict:

        volatility = market_data["volatility"]
        liquidity = market_data["liquidity"]

        risk_score = RiskAgent.compute_risk(volatility, liquidity)
        confidence = RiskAgent.compute_confidence(risk_score)

        return {
            "risk_score": risk_score,
            "confidence": confidence,
            "risk_level": RiskAgent.classify(risk_score),
        }

    @staticmethod
    def compute_risk(volatility, liquidity):
        return volatility * 100 - (liquidity / 1_000_000)

    @staticmethod
    def compute_confidence(risk_score):
        return max(0.0, min(1.0, 1 - (risk_score / 100)))

    @staticmethod
    def classify(risk_score):
        if risk_score < 20:
            return "low"
        elif risk_score < 50:
            return "medium"
        return "high"
