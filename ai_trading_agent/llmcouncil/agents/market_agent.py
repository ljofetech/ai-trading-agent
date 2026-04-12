from llmcouncil.client import LLMClient


class MarketAgent:

    @staticmethod
    def analyze(state: dict):
        user_input = state["user_input"]

        # Извлекаем торговую пару через ИИ
        extraction = LLMClient.generate(
            f"""
                Extract trading pair from message.

                Message: {user_input}

                Return ONLY valid JSON:
                    {{
                    "asset_in": "...",
                    "asset_out": "..."
                    }}
            """
        )

        asset_in = extraction["asset_in"]
        asset_out = extraction["asset_out"]
        timeframe = 1440

        pair = f"{asset_in}{asset_out}"

        # Собираем сырые данные с Kraken
        ticker_data = 0
        historical_data = 0

        # Передаем сырые данные ИИ для полного анализа
        analysis = LLMClient.generate(
            f"""
                You are a quantitative crypto analyst using Trend Following + ATR strategy.

                Analyze this raw market data and calculate ALL technical indicators.

                CURRENT MARKET DATA:
                - Price: {ticker_data.get('price', 0)}
                - Liquidity: {ticker_data.get('liquidity', 0)}
                - 24h Volume: {ticker_data.get('volume_24h', 0)}
                
                HISTORICAL PRICE DATA (last 100 candles, {timeframe} minute timeframe):
                {historical_data}

                Calculate the following using ONLY this data:
                1. ATR (Average True Range) for periods 7, 14, 21
                2. ATR percentage relative to current price
                3. SMA (Simple Moving Average): 10, 30, 50 periods
                4. EMA (Exponential Moving Average): 12, 26 periods
                5. Trend direction (bullish/bearish/neutral) with confidence score
                6. Trend strength (0-100)
                7. Volatility regime (low/medium/high/extreme)
                8. Support and resistance levels (nearest 3 each)
                9. Current price position relative to moving averages

                Return ONLY valid JSON with your calculations:
                {{
                    "asset_in": "{asset_in}",
                    "asset_out": "{asset_out}",
                    "timeframe": "{timeframe}",
                    "current_price": {ticker_data.get('price', 0)},
                    "liquidity": {ticker_data.get('liquidity', 0)},
                    "atr": {{
                        "period_7": number,
                        "period_14": number,
                        "period_21": number
                    }},
                    "atr_percent": number,
                    "sma": {{
                        "sma_10": number,
                        "sma_30": number,
                        "sma_50": number
                    }},
                    "ema": {{
                        "ema_12": number,
                        "ema_26": number
                    }},
                    "trend": {{
                        "direction": "bullish | bearish | neutral",
                        "confidence": number,
                        "strength": number,
                        "reasoning": "text"
                    }},
                    "volatility_regime": "low | medium | high | extreme",
                    "support_levels": [number, number, number],
                    "resistance_levels": [number, number, number],
                    "price_vs_ma": {{
                        "above_sma_10": boolean,
                        "above_sma_30": boolean,
                        "above_sma_50": boolean,
                        "distance_from_sma_30_percent": number
                    }}
                }}
            """
        )

        return analysis
