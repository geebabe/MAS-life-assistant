from openai import OpenAI
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        return self.generate_with_messages([
            {"role": "user", "content": prompt}
        ])

    def generate_with_messages(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

    def generate_structured(self, messages: list[dict], schema: dict):
        """
        Implementation of structured output using OpenAI JSON schema.
        Note: The schema should be a Pydantic-like dict or JSON schema.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "strict": True,
                    "schema": schema
                }
            }
        )
        return response.choices[0].message.content