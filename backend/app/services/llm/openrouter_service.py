from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def generate_response(query, context):

    prompt = f"""
You are a helpful research assistant.

Answer the user's question ONLY using the provided context.

If the answer is not in the context, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content