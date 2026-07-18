from app.models.message import Message


SYSTEM_PROMPT = """
You are Nebula.

You answer questions using the provided documents.

Rules:

- Only answer from DOCUMENT CONTEXT.
- If the answer is not in the document, say:
  "I couldn't find that information in the uploaded documents."
- Never invent facts.
- Be concise.
- Quote important values exactly.
""".strip()


def build_messages(
    history: list[Message],
    context: str = "",
) -> list[dict]:

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if context:
        messages.append(
            {
                "role": "system",
                "content": f"Document Context:\n\n{context}",
            }
        )

    for message in history:
        messages.append(
            {
                "role": message.role,
                "content": message.content,
            }
        )

    return messages