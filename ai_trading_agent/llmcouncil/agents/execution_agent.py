from llmcouncil.client import LLMClient


class ExecutionAgent:

    @staticmethod
    def plan(state: dict, market_data: dict, risk_data: dict):
        response = LLMClient.generate(
            f"""
                You are an expert crypto execution trader using Trend Following + ATR strategy.
                
                Create a COMPLETE trading plan based on the market and risk analysis.
                Think like a professional trader managing real money.

                USER CONTEXT:
                - User message: {state["user_input"]}
                
                MARKET ANALYSIS:
                {market_data}
                
                RISK ASSESSMENT:
                {risk_data}

                Create a detailed execution plan with:

                1. TRADE DECISION:
                   - Action: "BUY" | "SELL" | "HOLD" | "CLOSE_POSITION"
                   - Why this action now?
                   
                2. ENTRY STRATEGY:
                   - Entry price (market or limit)
                   - If limit: specify price and why
                   - Entry conditions (what needs to happen)
                   
                3. POSITION MANAGEMENT:
                   - Amount in USD or percentage
                   - Number of orders (1, 2, 3 for scaling)
                   - Scaling strategy
                   
                4. STOP LOSS:
                   - Price level
                   - ATR multiplier used
                   - Trailing stop? (yes/no, with parameters)
                   - Breakeven stop after X profit
                   
                5. TAKE PROFIT:
                   - 3-5 take profit levels with percentages
                   - For each level: how much to close (e.g., 30%, 30%, 40%)
                   - Trail remaining position?
                   
                6. TIMING:
                   - Immediate execution or wait for specific condition
                   - Time horizon for this trade (hours/days)
                   
                7. RISK MANAGEMENT RULES:
                   - Max position size for this trade
                   - Daily loss limit suggestion
                   - When to re-evaluate
                   
                8. ALTERNATIVE SCENARIOS:
                   - If price goes up X% before entry
                   - If price goes down X% before entry
                   - If volatility spikes
                   
                9. REASONING:
                   - Clear, conversational explanation
                   - Why this plan makes sense for trend following
                   
                10. CONFIDENCE:
                    - Your confidence in this plan (0-100)
                    
                11. SUCCESS CRITERIA:
                    - What defines a successful trade?

                Return ONLY valid JSON with your complete execution plan:
                {{
                    "asset_in": "{market_data.get('asset_in', '')}",
                    "asset_out": "{market_data.get('asset_out', '')}",
                    "decision": {{
                        "action": "BUY | SELL | HOLD | CLOSE_POSITION",
                        "reasoning": "text",
                        "confidence": number
                    }},
                    "entry": {{
                        "type": "market | limit",
                        "price": number,
                        "conditions": ["condition1", "condition2"],
                        "scaling": {{
                            "enabled": boolean,
                            "orders": [
                                {{"percent": number, "price_offset_percent": number}}
                            ]
                        }}
                    }},
                    "position": {{
                        "amount_usd": number,
                        "amount_percent": number,
                        "max_position_usd": number
                    }},
                    "stop_loss": {{
                        "initial_price": number,
                        "atr_multiplier": number,
                        "trailing": {{
                            "enabled": boolean,
                            "activation_percent": number,
                            "distance_percent": number
                        }},
                        "breakeven": {{
                            "enabled": boolean,
                            "after_profit_percent": number
                        }}
                    }},
                    "take_profit": [
                        {{
                            "level": number,
                            "price": number,
                            "close_percent": number,
                            "atr_multiplier": number
                        }}
                    ],
                    "timing": {{
                        "execution": "immediate | conditional",
                        "wait_condition": "text or null",
                        "time_horizon_hours": number
                    }},
                    "risk_rules": {{
                        "max_position_percent": number,
                        "daily_loss_limit_percent": number,
                        "re_evaluate_after_hours": number
                    }},
                    "alternative_scenarios": {{
                        "if_price_up_X_percent": "text",
                        "if_price_down_X_percent": "text",
                        "if_volatility_spikes": "text"
                    }},
                    "reasoning": "clear, conversational explanation for the user",
                    "success_criteria": "text",
                    "warnings": ["warning1", "warning2"],
                    "tags": ["trend_following", "atr", "momentum"]
                }}
            """
        )

        return response
