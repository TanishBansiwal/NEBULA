from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User

from app.schemas.message import (
    MessageCreate,
    MessageResponse,
)

from app.services.ai_service import GroqProvider
from app.services.conversation_service import get_conversation
from app.services.message_service import (
    create_message,
    get_message_history,
)
from app.services.prompt_service import build_messages

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

ai = GroqProvider()


@router.post(
    "/{conversation_id}",
    response_model=list[MessageResponse],
)
def chat(
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
    user_message = create_message(
        db,
        conversation_id,
        "user",
        data.content,
    )

    # Load conversation history
    history = get_message_history(
        db,
        conversation_id,
    )

    # Build prompt
    prompt = build_messages(history)

    # Generate AI response
    try:
        reply = ai.chat(prompt)

    except RuntimeError as e:
        raise HTTPException(
           status_code=503,
          detail=str(e),
    )

    # Save assistant message
    assistant_message = create_message(
        db,
        conversation_id,
        "assistant",
        reply,
    )

    return [
       user_message,
       assistant_message,
    ]

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
    user_message = create_message(
        db,
        conversation_id,
        "user",
        data.content,
    )
    # Load conversation history
    history = get_message_history(
        db,
        conversation_id,
    
    )
    # Build prompt
    prompt = build_messages(history)

    assistant_reply = ""


    def generator():
        nonlocal assistant_reply

        try:
            for chunk in ai.stream_chat(prompt):
                assistant_reply += chunk

                yield f"data: {chunk}\n\n"

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