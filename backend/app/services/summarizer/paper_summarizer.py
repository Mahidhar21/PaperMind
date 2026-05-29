import ollama

from app.services.pdf.chunker import chunk_text


def summarize_chunk(chunk):

    prompt = f"""
Summarize the following text clearly and concisely.

Text:
{chunk}
"""

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


def generate_final_summary(chunk_summaries):

    combined_summary = "\n\n".join(chunk_summaries)

    prompt = f"""
The following are partial summaries of different sections
of a document.

Generate one final detailed and coherent summary
covering the full document.

Partial Summaries:
{combined_summary}
"""

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


def generate_paper_summary(text):

    chunks = chunk_text(text)

    chunk_summaries = []

    for chunk in chunks:

        summary = summarize_chunk(
            chunk["text"]
        )

        chunk_summaries.append(summary)

    final_summary = generate_final_summary(
        chunk_summaries
    )

    return final_summary