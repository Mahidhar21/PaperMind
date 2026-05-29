from pathlib import Path
import pickle
import json
import ollama

from fastapi import APIRouter

router = APIRouter()

VECTOR_STORE_DIR = Path(
    "vector_store"
)


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


def extract_graph_from_text(text):

    prompt = f"""
    You are an expert knowledge graph extraction system.

    Extract ALL possible technical relationships.

    Find:

    - concepts
    - algorithms
    - data structures
    - methods
    - techniques
    - database components
    - indexing structures
    - optimizations
    - applications
    - comparisons

    Return AT LEAST 15 relationships.

    Return ONLY JSON.

    Format:

    [
        {{
            "source":"B+ Tree",
            "relation":"supports",
            "target":"Range Queries"
        }}
    ]

    Text:

    {text[:8000]}
    """ 

    result = generate_graph_response(
        prompt
    )

    try:

        start = result.find("[")

        end = result.rfind("]")

        if start == -1 or end == -1:
            return []

        json_text = result[start:end + 1]

        return json.loads(
            json_text
        )

    except Exception:

        print(
            "\nGRAPH PARSE FAILED\n"
        )

        print(result)

        return []


@router.get("/multi-graph")
async def generate_multi_graph():

    graph = []

    for docs_file in VECTOR_STORE_DIR.glob(
        "*.pkl"
    ):

        print(
            f"\nProcessing: {docs_file.name}"
        )

        with open(
            docs_file,
            "rb"
        ) as f:

            chunks = pickle.load(f)

        text = "\n".join([
            chunk["text"]
            for chunk in chunks[:50]
        ])

        relationships = extract_graph_from_text(
            text
        )

        graph.extend(
            relationships
        )

    seen = set()

    unique_graph = []

    for edge in graph:

        try:

            key = (
                edge["source"],
                edge["relation"],
                edge["target"]
            )

            if key not in seen:

                seen.add(key)

                unique_graph.append(
                    edge
                )

        except Exception:

            continue

    print(
        f"\nTOTAL EDGES: {len(unique_graph)}\n"
    )

    return {
        "graph": unique_graph
    }