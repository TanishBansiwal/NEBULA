import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.services.pdf_service import extract_pdf_text
from app.services.chunker import chunk_text
from app.services.embeddings import embed_chunks


UPLOAD_DIR = "app/storage/uploads"



def save_document(
    db: Session,
    conversation_id: int,
    file: UploadFile,
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    extension = os.path.splitext(file.filename)[1]

    unique_name = f"{uuid.uuid4()}{extension}"

    path = os.path.join(
        UPLOAD_DIR,
        unique_name,
    )
   

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer, )
   
   
    content = ""
    chunks = []
    embeddings = []

    if file.content_type == "application/pdf":
        content = extract_pdf_text(path)

        chunks = chunk_text(content)

        embeddings = embed_chunks(chunks)

    document = Document(
        conversation_id=conversation_id,
        filename=file.filename,
        filepath=path,
        filetype=file.content_type,
        filesize=file.size,
        content=content,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        db.add(
        DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk,
            embedding=embedding,
        )
    )

    db.commit()

    return document