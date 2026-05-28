from pathlib import Path

from app.services.pdf.extractor import (
    extract_text_from_pdf
)

from app.services.pdf.chunker import (
    chunk_text
)

from app.services.embeddings.embedder import (
    generate_embedding
)

from app.services.vectorstore.faiss_store import (
    FAISSVectorStore
)


VECTOR_STORE_DIR = Path(
    "vector_store"
)

VECTOR_STORE_DIR.mkdir(
    exist_ok=True
)


def build_vector_database(pdf_path):

    filename = Path(pdf_path).stem

    index_path = VECTOR_STORE_DIR / f"{filename}.index"

    docs_path = VECTOR_STORE_DIR / f"{filename}.pkl"

    extracted_text = extract_text_from_pdf(
        pdf_path
    )

    chunks = chunk_text(
        extracted_text
    )

    embeddings = []

    chunk_data = []

    for chunk in chunks:

        embedding = generate_embedding(
            chunk["text"]
        )

        embeddings.append(
            embedding
        )

        chunk_data.append(
            chunk
        )

    dimension = len(
        embeddings[0]
    )

    vector_store = FAISSVectorStore(
        dimension
    )

    vector_store.add_embeddings(
        embeddings,
        chunk_data
    )

    vector_store.save(
        str(index_path),
        str(docs_path)
    )

    return {
        "index_path": str(index_path),
        "docs_path": str(docs_path),
        "chunks": len(chunk_data)
    }