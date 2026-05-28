import google.generativeai as genai

from app.core.config import settings


genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel("gemini-2.0-flash")


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

    response = model.generate_content(prompt)

    return response.text