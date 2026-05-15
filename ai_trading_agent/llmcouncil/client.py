# Import modules for JSON handling, environment variables, regex, and the OpenRouter client
import json
import os
import re
from dotenv import load_dotenv
from openrouter import OpenRouter

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("AI_API_KEY")

# System prompt that instructs the LLM to act as a strict JSON-only trading agent
SYSTEM_PROMPT = """
You are an automated multi-role trading AI. You operate inside a structured pipeline (LLMCouncil) and will be assigned tasks as a Market Analyst, Risk Assessor, Execution Planner, or Supervisor. 

Rules you must follow:
- Your entire response must be valid JSON, parseable by json.loads.
- Never add any text before or after the JSON, no markdown fences, no explanations, no greetings.
- Output only the exact JSON object requested in the prompt, with the exact keys and data types specified.
- Do not include disclaimers, advice, or suggestions outside the requested structure.
- Remember: your output is consumed directly by a trading system; any deviation will break the pipeline.
"""


class LLMClient:

    @staticmethod
    def generate(prompt: str):
        # Open a connection to the OpenRouter API using the environment key
        with OpenRouter(api_key=api_key) as client:

            # Send the system prompt and the user prompt to the specified model
            response = client.chat.send(
                model="deepseek/deepseek-chat-v3.1",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )

            # Extract the raw text content from the first (and only) choice
            content = response.choices[0].message.content

            # Fail early if the response is empty
            if not content:
                raise ValueError("LLM returned empty response")

            # Clean the text: strip whitespace and remove markdown fences if present
            text = content.strip()
            text = text.replace("```json", "").replace("```", "").strip()

            try:
                # Attempt to parse the cleaned text as JSON
                return json.loads(text)

            except json.JSONDecodeError:
                # If direct parsing fails, try to find a JSON object using regex
                match = re.search(r"\{.*\}", text, re.DOTALL)

                if match:
                    try:
                        return json.loads(match.group())
                    except json.JSONDecodeError:
                        pass  # if even the regex match fails, fall through to raise an error

                # Raise an error if no valid JSON could be extracted
                raise ValueError(f"Model did not return valid JSON:\n{text}")
