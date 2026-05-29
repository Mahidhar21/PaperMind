import ollama


def generate_response(query, context, history):

    messages = []

    system_prompt = f"""
You are a helpful research assistant.

Answer the user's question using the provided context.

Be concise and factual.

If relevant information exists in the context,
use it to construct the answer.

Context:
{context}
"""

    messages.append({
        "role": "system",
        "content": system_prompt
    })

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": query
    })

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=messages
    )

    print(context[:1000])

    return response["message"]["content"]


def stream_response(query, context, history):

    messages = []

    system_prompt = f"""
You are a helpful research assistant.

Answer the user's question using the provided context.

Be concise and factual.

If relevant information exists in the context,
use it to construct the answer.

Context:
{context}
"""

    messages.append({
        "role": "system",
        "content": system_prompt
    })

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": query
    })

    stream = ollama.chat(
        model="qwen2.5:3b",
        messages=messages,
        stream=True
    )

    for chunk in stream:

        content = chunk["message"]["content"]

        yield content