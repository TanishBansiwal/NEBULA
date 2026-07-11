from abc import ABC, abstractmethod


class AIProvider(ABC):
    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        pass


class MockAIProvider(AIProvider):
    def chat(self, messages: list[dict]) -> str:
        user_message = messages[-1]["content"]

        return f"You said: {user_message}"