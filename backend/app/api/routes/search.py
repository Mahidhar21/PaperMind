from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.services.pdf.extractor import extract_text_from_pdf
from app.services.pdf.chunker import chunk_text
from app.services.embeddings.embedder import generate_embedding
from app.services.vectorstore.faiss_store import FAISSVectorStore

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.get("/search/{filename}")
async def search_pdf(filename: str, query: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    extracted_text = extract_text_from_pdf(str(file_path))

    chunks = chunk_text(extracted_text)

    embeddings = []

    chunk_texts = []

    for chunk in chunks:

        embedding = generate_embedding(chunk["text"])

        embeddings.append(embedding)

        chunk_texts.append(chunk)

    dimension = len(embeddings[0])

    vector_store = FAISSVectorStore(dimension)

    vector_store.add_embeddings(
        embeddings,
        chunk_texts
    )

    query_embedding = generate_embedding(query)

    results = vector_store.search(query_embedding)

    return {
        "query": query,
        "results": results
    }