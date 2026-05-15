# Import json for serialization and the LLM client to generate a trading plan
import json
from llmcouncil.client import LLMClient


class ExecutionAgent:

    @staticmethod
    def plan(
        state: dict,  # original conversation state (contains user_input)
        market_data: dict,  # output from MarketAgent (history + predictions)
        risk_data: dict,  # output from RiskAgent (risk scores, leverage, etc.)
    ):
        print(
            "\n[ExecutionAgent] Formulating execution plan based on market analysis and risk assessment..."
        )
        # Retrieve the original user message for additional context
        user_input = state.get("user_input", "")

        # Extract the latest closing price from historical candles (or fallback to 0)
        history = market_data.get("history", [])
        if history and isinstance(history[-1], dict):
            last_close = history[-1].get("close", 0)
        else:
            last_close = 0

        # Serialize predictions and risk assessment to JSON strings for the prompt
        prediction_json = json.dumps(market_data.get("prediction", []), default=str)
        risk_json = json.dumps(risk_data, default=str)
        print("Market predictions and risk assessment prepared for execution planning.")
        # Ask the LLM to formulate a concrete trading plan based on all available data
        response = LLMClient.generate(f"""
            You are an expert futures execution trader.
            Given the user request, market data, and risk assessment, create a precise trading plan.

            User request: {user_input}
            Latest close price: {last_close}
            Price predictions: {prediction_json}
            Risk assessment: {risk_json}

            Your plan must include:
            - Action: "BUY" (go long), "SELL" (go short), or "HOLD" (no trade).
            - Entry conditions: if limit order, state target entry price and logic; if market, say "market".
            - Stop-loss price (absolute value or trailing description) – align with risk_assessment stop_loss_pct.
            - Take-profit price(s) (can be multiple levels) – align with risk_assessment take_profit_pct.
            - Position size (in base asset, e.g., BTC amount) – derived from risk percentage and account size. Assume a virtual account size of 10,000 USDT for sizing.
            - Leverage: the exact leverage to use (must not exceed max_leverage from risk).
            - Trade duration estimate (e.g., "4 hours").
            - Reasoning: short justification.

            Important: Ensure stop-loss and take-profit are on the correct side depending on direction (long or short).

            Return ONLY valid JSON with keys:
            {{
                "action": "BUY" | "SELL" | "HOLD",
                "entry_type": "market" | "limit",
                "entry_price": number or null (if market, set to current close),
                "stop_loss": number,
                "take_profit": [list of price targets],
                "position_size": number (base asset quantity),
                "leverage": integer,
                "trade_duration": "string",
                "reasoning": "string"
            }}
            """)
        print("Execution plan generated with the following details:")
        print(response)
        # Return the LLM's trading plan (expected as a JSON object)
        return response
