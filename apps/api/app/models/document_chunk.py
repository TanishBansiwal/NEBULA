from sqlalchemy import (Column, Integer, Text, ForeignKey,)

from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index = Column(Integer, nullable=False)

    content = Column(Text, nullable=False)

    embedding = Column(
        Vector(768),      # change if your embedding model uses another dimension
        nullable=False,
    )

    document = relationship(
        "Document",
        back_populates="chunks",
    )