import ollama

from app.config import settings


SYSTEM_PROMPT = (
    "You are a finance assistant for the PennyWise app. Use the provided "
    "context for finance facts, rules, and definitions, and mention a source "
    "document only if you actually used it. If the user gives their own "
    "numbers, such as shares, prices, or amounts, you may do simple "
    "arithmetic with them and show the steps, even if the context has no "
    "worked example. Never invent facts such as current stock prices, tax "
    "rates, or company data. If a needed fact is missing, say so plainly. "
    "Keep answers clear and simple. This is general education, not "
    "financial advice."
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

