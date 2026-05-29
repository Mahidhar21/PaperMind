from pathlib import Path

from fastapi import APIRouter

from app.services.embeddings.embedder import (
    generate_embedding
)

from app.services.vectorstore.faiss_store import (
    FAISSVectorStore
)

from app.services.llm.ollama_service import (
    generate_response
)

router = APIRouter()

VECTOR_STORE_DIR = Path(
    "vector_store"
)


@router.get("/multi-chat")
async def multi_chat(query: str):

    query_embedding = generate_embedding(
        query
    )

    all_chunks = []

    index_files = list(
        VECTOR_STORE_DIR.glob("*.index")
    )

    for index_file in index_files:

        pdf_name = index_file.stem

        docs_file = (
            VECTOR_STORE_DIR /
            f"{pdf_name}.pkl"
        )

        vector_store = FAISSVectorStore(
            dimension=384
        )

        vector_store.load(
            str(index_file),
            str(docs_file)
        )

        chunks = vector_store.search(
            query_embedding,
            top_k=3
        )

        for chunk in chunks:

            chunk["source_pdf"] = pdf_name

            all_chunks.append(
                chunk
            )

    context = "\n\n".join([
        chunk["text"]
        for chunk in all_chunks[:10]
    ])

    answer = generate_response(
        query=query,
        context=context,
        history=[]
    )

    return {
        "query": query,
        "answer": answer,
        "sources": [
            {
                "pdf": chunk["source_pdf"],
                "page": chunk["page"]
            }
            for chunk in all_chunks[:10]
        ]
    }