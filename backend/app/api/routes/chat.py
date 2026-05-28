from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.services.embeddings.embedder import (
    generate_embedding
)

from app.services.vectorstore.faiss_store import (
    FAISSVectorStore
)

from app.services.memory.chat_memory import (
    add_message,
    get_chat_history
)

from app.services.llm.ollama_service import (
    generate_response
)

router = APIRouter()

VECTOR_STORE_DIR = Path(
    "vector_store"
)


@router.get("/chat/{filename}")

async def chat_with_pdf(
    filename: str,
    query: str,
    session_id: str
):

    pdf_name = Path(filename).stem

    index_path = VECTOR_STORE_DIR / f"{pdf_name}.index"

    docs_path = VECTOR_STORE_DIR / f"{pdf_name}.pkl"

    if not index_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Vector database not found"
        )

    query_embedding = generate_embedding(
        query
    )

    vector_store = FAISSVectorStore(
        dimension=384
    )

    vector_store.load(
        str(index_path),
        str(docs_path)
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

    answer = generate_response(
        query=query,
        context=context,
        history=history
    )

    add_message(
        session_id,
        "user",
        query
    )

    add_message(
        session_id,
        "assistant",
        answer
    )

    return {
        "query": query,
        "answer": answer,
        "sources": relevant_chunks
    }