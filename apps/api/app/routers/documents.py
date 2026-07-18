from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User

from app.schemas.document import DocumentResponse

from app.services.conversation_service import get_conversation
from app.services.document_service import save_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload/{conversation_id}",
    response_model=DocumentResponse,
)
def upload_document(
    conversation_id: int,
    file: UploadFile = File(...),
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

    return save_document(
        db,
        conversation_id,
        file,
    )