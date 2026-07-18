from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embeddings import embed_chunks


def search_document_chunks(
    db: Session,
    conversation_id: int,
    query: str,
    limit: int = 5,
):
    # Create embedding for the user's question
    embedding = embed_chunks([query])[0]

    sql = text("""
        SELECT
        d.filename,
        dc.chunk_index,
        dc.content,
        dc.embedding <=> CAST(:embedding AS vector) AS distance
    FROM document_chunks dc
    JOIN documents d
        ON dc.document_id = d.id
    WHERE d.conversation_id = :conversation_id
    ORDER BY dc.embedding <=> CAST(:embedding AS vector)
    LIMIT :limit;
    """)

    result = db.execute(
        sql,
        {
            "embedding": embedding,
            "conversation_id": conversation_id,
            "limit": limit,
        },
    )

    return result.fetchall()