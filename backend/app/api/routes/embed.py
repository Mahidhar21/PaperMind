from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.services.pdf.extractor import extract_text_from_pdf
from app.services.pdf.chunker import chunk_text
from app.services.embeddings.embedder import generate_embedding

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.get("/embed/{filename}")
async def embed_pdf(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    extracted_text = extract_text_from_pdf(str(file_path))

    chunks = chunk_text(extracted_text)

    embedded_chunks = []

    for chunk in chunks:

        embedding = generate_embedding(chunk["text"])

        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "embedding_dimension": len(embedding)
        })

    return {
        "filename": filename,
        "total_chunks": len(embedded_chunks),
        "chunks": embedded_chunks
    }