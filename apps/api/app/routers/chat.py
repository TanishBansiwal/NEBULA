from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User

from app.schemas.message import MessageCreate
from app.schemas.search import SearchRequest

from app.services.retrieval_service import search_document_chunks
from app.services.ai_service import GroqProvider
from app.services.conversation_service import get_conversation
from app.services.message_service import (
    create_message,
    get_message_history,
)
from app.services.prompt_service import build_messages
from app.services.retrieval_service import search_document_chunks

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

ai = GroqProvider()


@router.post("/{conversation_id}/stream")
def stream_chat(
    conversation_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = get_conversation(
        db,
        conversation_id,
        current_user.id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # Save user message
    create_message(
        db,
        conversation_id,
        "user",
        data.content,
    )

    # Load history
    history = get_message_history(db, conversation_id,)

    results = search_document_chunks(  db=db, conversation_id=conversation_id, query=data.content, limit=5,)

    document_context = ""

    for row in results:
        document_context += (
            f"Document: {row.filename}\n"
            f"Chunk: {row.chunk_index}\n"
            f"{row.content}\n\n"
        )

    prompt = build_messages(
        history=history,
        context=document_context,
    )

    assistant_reply = ""

    sources = []

    for row in results:
        sources.append(
            f"{row.filename} (Chunk {row.chunk_index})"
        )

    def generator():
        nonlocal assistant_reply

        try:
            for chunk in ai.stream_chat(prompt):
                assistant_reply += chunk
                yield f"data: {chunk}\n\n"

            if sources:
                assistant_reply += "\n\nSources:\n"

                for source in sorted(set(sources)):
                    assistant_reply += f"- {source}\n"

            create_message(
                db,
                conversation_id,
                "assistant",
                assistant_reply,
            )

            yield "data: [DONE]\n\n"

        except RuntimeError as e:
            yield f"data: ERROR: {str(e)}\n\n"

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
    )

@router.post("/search")
def search_chunks(
    conversation_id: int,
    data: SearchRequest,
    db: Session = Depends(get_db),
):
    results = search_document_chunks(
        db=db,
        conversation_id=conversation_id,
        query=data.content,
        limit=5,
    )

    return {
        "results": [
            {
                "content": row.content,
                "distance": row.distance,
            }
            for row in results
        ]
    }