from app.models.message import Message


SYSTEM_PROMPT = """
You are Nebula.

You are a helpful, intelligent AI assistant.

Answer clearly and concisely.

If you don't know something, say so.

Never invent facts.
""".strip()


def build_messages(history: list[Message]) -> list[dict]:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for message in history:
        messages.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )

    return messages