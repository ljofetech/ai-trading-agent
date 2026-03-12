import json
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class LLMClient:

    @staticmethod
    def generate_json(prompt: str):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a crypto trading AI. Always return JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            extra_headers={
                "X-Client-Request-Id": "123e4567-e89b-12d3-a456-426614174000"
            },
        )

        content = response.choices[0].message.content

        return json.loads(content)
