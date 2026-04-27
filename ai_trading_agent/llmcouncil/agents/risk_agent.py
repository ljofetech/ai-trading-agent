# from llmcouncil.client import LLMClient


# class RiskAgent:

#     @staticmethod
#     def evaluate(market_data: dict):
#         analysis = LLMClient.generate(
#             f"""
#                 You are a professional risk manager for Trend Following + ATR strategy.
                
#                 Analyze this market data and calculate comprehensive risk metrics.
#                 Use your understanding of quantitative risk management and crypto markets.

#                 MARKET DATA:
#                 {market_data}

#                 Calculate the following risk metrics using YOUR OWN REASONING:
                
#                 1. RISK SCORE (0-100):
#                    - 0-30: Low risk - ideal for entry
#                    - 31-60: Medium risk - careful entry
#                    - 61-100: High risk - avoid or tiny position
                   
#                 2. CONFIDENCE SCORE (0-100):
#                    How confident are you in this risk assessment?
                   
#                 3. RISK LEVEL: "low" | "medium" | "high"
                
#                 4. POSITION SIZING (percent of portfolio):
#                    Based on ATR, trend strength, and your risk assessment
                   
#                 5. STOP LOSS MULTIPLIER (ATR multiplier):
#                    - 1.0-1.5: Tight stop (low volatility)
#                    - 1.5-2.5: Standard stop (normal volatility)
#                    - 2.5-4.0: Wide stop (high volatility, strong trend)
                   
#                 6. TAKE PROFIT MULTIPLIERS (ATR multipliers):
#                    Suggest 3 take profit levels for trend following
                   
#                 7. RISK-REWARD RATIO:
#                    Calculate minimum and expected R:R
                   
#                 8. MAX DRAWDOWN ESTIMATE:
#                    Expected maximum drawdown for this trade
                   
#                 9. VOLATILITY ADJUSTMENT:
#                    Recommended adjustment to position size based on volatility
                   
#                 10. LIQUIDITY RISK:
#                     Assessment of slippage and execution risk
                   
#                 11. CORRELATION RISK:
#                     If this is a stablecoin pair or correlated with BTC/ETH
                    
#                 12. FINAL RECOMMENDATION:
#                     "ENTER" | "AVOID" | "REDUCE_SIZE" | "WAIT"

#                 Return ONLY valid JSON with your professional risk assessment:
#                 {{
#                     "risk_score": number,
#                     "confidence": number,
#                     "risk_level": "low | medium | high",
#                     "recommended_position_size_percent": number,
#                     "stop_loss_atr_multiplier": number,
#                     "take_profit_multipliers": [number, number, number],
#                     "risk_reward_ratio": {{
#                         "minimum": number,
#                         "expected": number
#                     }},
#                     "max_drawdown_estimate_percent": number,
#                     "volatility_adjustment_factor": number,
#                     "liquidity_risk": "low | medium | high",
#                     "liquidity_risk_reasoning": "text",
#                     "correlation_risk": "low | medium | high",
#                     "final_recommendation": "ENTER | AVOID | REDUCE_SIZE | WAIT",
#                     "reasoning": "detailed explanation of your risk assessment",
#                     "warnings": ["warning1", "warning2"],
#                     "optimal_entry_conditions": ["condition1", "condition2"]
#                 }}
#             """
#         )

#         return analysis
