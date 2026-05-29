from fastapi import APIRouter
from pathlib import Path

from app.services.llm.ollama_service import (
    generate_response
)

router = APIRouter()

VECTOR_STORE_DIR = Path(
    "vector_store"
)

import ollama


def generate_graph_response(prompt):

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


@router.get("/graph/{filename}")
async def generate_graph(
    filename: str
):

    pdf_name = Path(filename).stem

    docs_file = (
        VECTOR_STORE_DIR /
        f"{pdf_name}.pkl"
    )

    import pickle

    with open(
        docs_file,
        "rb"
    ) as f:

        chunks = pickle.load(f)

    text = "\n".join([
        chunk["text"]
        for chunk in chunks
    ])

    prompt = f"""
        You are an information extraction system.

        Extract entities and relationships.

        Return ONLY a JSON array.

        Do not explain anything.
        Do not add markdown.
        Do not add text before or after JSON.

        Example:

        [
        {{
            "source":"B+ Tree",
            "relation":"used_for",
            "target":"Indexing"
        }}
        ]

        Text:

        {text}
        """

    result = generate_graph_response(
        prompt
    )

    import json

    try:

        graph = json.loads(result)

    except:

        graph = []

    return {
        "graph": graph
    }