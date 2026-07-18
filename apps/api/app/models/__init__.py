from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.core.database import Base, engine



#Base.metadata.create_all(bind=engine)