from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User

from app.schemas.message import (
    MessageCreate,
    MessageResponse,
)

from app.services.ai_service import MockAIProvider
from app.services.conversation_service import get_conversation
from app.services.message_service import (
    create_message,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

ai = MockAIProvider()


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

    # Generate AI response
    reply = ai.chat(
        [{"role": "user", "content": data.content}]
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