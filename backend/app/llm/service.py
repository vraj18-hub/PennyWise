import ollama

from app.config import settings

SYSTEM_PROMPT = (
    "You are a finance assistant for the PennyWise app. Answer the user's "
    "question using ONLY the context provided below. Be clear and simple, "
    "and include a numeric example if it helps. If the context does not "
    "contain enough information to answer, say so honestly instead of "
    "guessing. Always mention which source document(s) you used."
)


def generate_answer(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return (
            "I don't have any information on that topic in my knowledge "
            "base yet."
        )

    context_parts = []
    for chunk in chunks:
        context_parts.append(f"{chunk['text']}\n(Source: {chunk['source']})")
    context = "\n\n".join(context_parts)

    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    response = ollama.chat(
        model=settings.LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response["message"]["content"]