from abc import ABC, abstractmethod

from openai import OpenAI
from openai import APIError
from openai import RateLimitError
from openai import AuthenticationError

from app.core.config import settings


class AIProvider(ABC):
    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        pass


class GroqProvider(AIProvider):
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

    def chat(self, messages: list[dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
            )

            return response.choices[0].message.content

        except AuthenticationError:
            raise RuntimeError("Invalid Groq API key.")

        except RateLimitError:
            raise RuntimeError("Groq rate limit exceeded.")

        except APIError:
            raise RuntimeError("Groq API is unavailable.")

        except Exception as e:
            raise RuntimeError(f"Unexpected AI service error: {e}")

    def stream_chat(self, messages: list[dict]):
        try:
            stream = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content

                if delta:
                    yield delta

        except AuthenticationError:
            raise RuntimeError("Invalid Groq API key.")

        except RateLimitError:
            raise RuntimeError("Groq rate limit exceeded.")

        except APIError:
            raise RuntimeError("Groq API is unavailable.")

        except Exception as e:
            raise RuntimeError(f"Unexpected AI service error: {e}")