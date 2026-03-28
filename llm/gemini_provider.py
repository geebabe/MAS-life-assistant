from google import genai
from google.genai import types
from .base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model


    def generate(self, prompt: str) -> str:
        return self.generate_with_messages([
            {"role": "user", "content": prompt}
        ])


    def generate_with_messages(self, messages: list[dict]) -> str:
        system_instruction = None
        contents = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                system_instruction = content
            else:
                contents.append({
                    "role": "user" if role == "user" else "system",
                    "parts": [{"text": content}]
                })

        if not contents:
            return ""

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.777
            )
        )

        return response.text or ""

    def generate_structured(self, messages: list[dict], schema):
        system_instruction = None
        contents = []

        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                contents.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [{"text": msg["content"]}]
                })

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0
            )
        )

        if response.parsed:
            return response.parsed

        return response.text

