from sqlalchemy.orm import Session

from app.models.document import Document


def get_conversation_context(
    db: Session,
    conversation_id: int,
) -> str:

    docs = (
        db.query(Document)
        .filter(Document.conversation_id == conversation_id)
        .all()
    )

    context = ""

    for doc in docs:
        if doc.content:
            context += doc.content + "\n\n"

    return context