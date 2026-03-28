import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm import get_llm_provider, BaseLLMProvider, OpenAIProvider, GeminiProvider
from config import config

def test_factory():
    print(f"Testing for provider: {config.LLM_PROVIDER}")
    provider = get_llm_provider()
    print(f"Provider class: {type(provider)}")
    
    if config.LLM_PROVIDER == "openai":
        assert isinstance(provider, OpenAIProvider)
    elif config.LLM_PROVIDER == "gemini":
        assert isinstance(provider, GeminiProvider)
    
    # Testing interface adherence
    assert hasattr(provider, "generate")
    assert hasattr(provider, "generate_with_messages")
    print("Factory test passed!")

if __name__ == "__main__":
    test_factory()
