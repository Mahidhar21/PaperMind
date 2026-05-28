import ollama


def generate_response(query, context, history):

    messages = []

    system_prompt = f"""
You are a helpful research assistant.

Answer the user's question ONLY using the provided context.

If the answer is not in the context, say:
"I could not find the answer in the document."

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
        model="tinyllama",
        messages=messages
    )

    return response["message"]["content"]