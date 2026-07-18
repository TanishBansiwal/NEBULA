from sqlalchemy import (Column, Integer, String, ForeignKey, DateTime,)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base
from sqlalchemy import Text

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    filename = Column(String, nullable=False)

    filepath = Column(String, nullable=False)

    filetype = Column(String, nullable=False)

    filesize = Column(Integer)

    content = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(),)

    conversation = relationship( "Conversation", back_populates="documents",)

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan",)