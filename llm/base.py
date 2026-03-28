from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generates a response for a single prompt string."""
        pass

    @abstractmethod
    def generate_with_messages(self, messages: list[dict]) -> str:
        """Generates a response for a list of message objects."""
        pass

    @abstractmethod
    def generate_structured(self, messages: list[dict], schema: dict):
        """Generates a structured response based on a schema."""
        pass
