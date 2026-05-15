import json  # For serializing market data to JSON strings
from llmcouncil.client import LLMClient  # LLM client to perform risk analysis


class RiskAgent:

    @staticmethod
    def evaluate(market_data: dict):
        print("\n[RiskAgent] Evaluating risk based on market analysis...")
        # Extract historical candles and prediction data from the market analysis output
        history_data = market_data.get("history", [])
        prediction_data = market_data.get("prediction", [])

        # If history is too long, keep only the last 200 candles to stay within token limits
        if len(history_data) > 200:
            history_data = history_data[-200:]

        # Convert both datasets to JSON strings for inclusion in the prompt
        history_json = json.dumps(history_data, default=str)
        prediction_json = json.dumps(prediction_data, default=str)
        print(
            f"History data (last {len(history_data)} candles) and predictions prepared for risk evaluation."
        )
        # Send a structured prompt to the LLM asking for a comprehensive risk evaluation
        analysis = LLMClient.generate(f"""
            You are a senior risk analyst for crypto futures trading.
            Analyze the provided historical OHLCV candles and price predictions for the next forecast horizon.

            Historical candles (last {len(history_data)} periods):
            {history_json}

            Price predictions (timestamp and forecasted values, possibly with confidence intervals):
            {prediction_json}

            Your task:
            1. Calculate current market volatility (e.g., ATR based on historical data or predicted range).
            2. Evaluate trend strength and potential reversals.
            3. Assess the risk of the trade: consider maximum adverse excursion, forecast uncertainty, and liquidity.
            4. Provide a risk score from 1 (very safe) to 10 (extremely risky).
            5. Suggest a maximum leverage and a safe stop-loss distance (in percentage from entry).
            6. Indicate if trading is recommended at all (allowed = true/false).

            Return ONLY valid JSON with the following keys:
            {{
                "risk_score": number,
                "volatility_pct": number (annualized or period-based, e.g. recent price range as % of price),
                "max_leverage": integer (1-125, default 5 if low risk, 1 if high risk),
                "stop_loss_pct": number (e.g. 1.5 meaning 1.5%),
                "take_profit_pct": number (e.g. 3.0),
                "trading_allowed": boolean,
                "warnings": [list of strings]
            }}

            Respond ONLY with the JSON. No additional text.
            """)
        print("Risk evaluation completed with the following analysis:")
        print(analysis)
        # Return the LLM's risk evaluation (expected to be a JSON object)
        return analysis
