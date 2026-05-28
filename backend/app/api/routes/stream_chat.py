from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from pathlib import Path

from app.services.pdf.extractor import extract_text_from_pdf
from app.services.pdf.chunker import chunk_text

from app.services.embeddings.embedder import generate_embedding
from app.services.vectorstore.faiss_store import FAISSVectorStore

from app.services.memory.chat_memory import (
    add_message,
    get_chat_history
)

from app.services.llm.ollama_service import (
    stream_response
)

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.get("/stream-chat/{filename}")
async def stream_chat(
    filename: str,
    query: str,
    session_id: str
):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    extracted_text = extract_text_from_pdf(
        str(file_path)
    )

    chunks = chunk_text(extracted_text)

    embeddings = []

    chunk_data = []

    for chunk in chunks:

        embedding = generate_embedding(
            chunk["text"]
        )

        embeddings.append(embedding)

        chunk_data.append(chunk)

    dimension = len(embeddings[0])

    vector_store = FAISSVectorStore(
        dimension
    )

    vector_store.add_embeddings(
        embeddings,
        chunk_data
    )

    query_embedding = generate_embedding(
        query
    )

    relevant_chunks = vector_store.search(
        query_embedding
    )

    context = "\n\n".join([
        chunk["text"]
        for chunk in relevant_chunks
    ])

    history = get_chat_history(
        session_id
    )

    generator = stream_response(
        query=query,
        context=context,
        history=history
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )