from sqlalchemy.orm import Session

from app.analytics.service import compute_summary
from app.llm.service import SYSTEM_PROMPT
from app.rag.vectorstore import search
import ollama
from app.config import settings

INSIGHT_SYSTEM_PROMPT = (
    "You are a personal finance coach inside the PennyWise app. You are given "
    "a summary of the user's real spending, and some general finance "
    "knowledge relevant to their question. Use BOTH to give clear, specific, "
    "personalized advice. Include actual numbers from their situation where "
    "relevant. Mention the source document(s) for any general concept you "
    "use. If the retrieved knowledge doesn't cover the question, say so "
    "honestly, but still comment on their numbers if you can. This is not "
    "financial advice, only general guidance."
)


def generate_insight(db: Session, user_id: int, question: str) -> str:
    summary = compute_summary(db, user_id)
    chunks = search(question, n_results=3)

    summary_text = (
        f"Total income: {summary['total_income']}\n"
        f"Total expenses: {summary['total_expenses']}\n"
        f"Savings rate: {summary['savings_rate']}%\n"
        f"Spending by category: "
        + ", ".join(
            f"{c['category']}: {c['total']}" for c in summary["by_category"]
        )
    )

    if chunks:
        knowledge_text = "\n\n".join(
            f"{c['text']}\n(Source: {c['source']})" for c in chunks
        )
    else:
        knowledge_text = "No specific documents found for this question."

    user_message = (
        f"User's financial summary:\n{summary_text}\n\n"
        f"Relevant finance knowledge:\n{knowledge_text}\n\n"
        f"User's question: {question}"
    )

    response = ollama.chat(
        model=settings.LLM_MODEL,
        messages=[
            {"role": "system", "content": INSIGHT_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response["message"]["content"]