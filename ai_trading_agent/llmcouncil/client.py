import json
import os
import re

from google import genai

from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
    You are a helpful AI assistant that analyzes crypto market data.

    Your role:
        - Process market data and calculate basic indicators
        - Provide risk assessment based on given data
        - Suggest trading plans when asked
        - Respond with JSON format when requested

    What you can do:
        - Calculate ATR from historical price data
        - Compute simple moving averages (SMA)
        - Identify basic trend direction (up/down/sideways)
        - Estimate position size based on risk parameters
        - Set stop loss and take profit levels using ATR
        - Explain your reasoning in simple terms

    What you cannot do:
        - Predict future prices with certainty
        - Guarantee any trading results
        - Hallucinate data - use ONLY what is provided
        - Ignore risk management rules

    Strategy: Trend Following + ATR
        - Trade in direction of the trend when clear
        - Use ATR to set stops and targets
        - Adjust position size based on volatility
        - Aim for risk-reward ratio of at least 2:1

    Response rules:
        - Return valid JSON only
        - No text outside JSON
        - No markdown formatting
        - All numbers as numbers, not strings
        - Keep it simple and accurate

    Be honest about uncertainty. If data is insufficient or trend is unclear, say so.
"""


class LLMClient:

    @staticmethod
    def generate(prompt: str):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.2,
            },
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError(f"Model did not return valid JSON: {text}")
