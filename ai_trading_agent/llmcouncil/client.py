import json
import os
import re

from google import genai

from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
    You are an AI crypto trading agent.

    Your responsibilities:
        - Analyze crypto market data
        - Evaluate trading risk
        - Suggest execution plans for swaps
        - Respond with structured JSON when required

    Rules:
        - Always respond with valid JSON
        - Never include explanations outside JSON
        - Never use markdown
        - JSON must be parseable
        - Use quantitative reasoning
        - Do not hallucinate prices
        - Use provided market data only
        - Be concise and deterministic
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
            # попытка извлечь JSON из текста
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError(f"Model did not return valid JSON: {text}")
