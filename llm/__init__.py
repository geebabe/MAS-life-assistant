from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .base import BaseLLMProvider
from config import config

def get_llm_provider() -> BaseLLMProvider:
    provider = config.LLM_PROVIDER
    if provider == "openai":
        return OpenAIProvider(
            api_key=config.OPENAI_API_KEY,
            model=getattr(config, "DEFAULT_OPENAI_MODEL", "gpt-4o")
        )
    elif provider == "gemini":
        return GeminiProvider(
            api_key=config.GEMINI_API_KEY,
            model=getattr(config, "DEFAULT_GEMINI_MODEL", "gemini-1.5-pro")
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
