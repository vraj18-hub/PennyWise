from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.db.models import User
from app.llm.service import generate_answer
from app.rag.schemas import AskRequest, AskResponse
from app.rag.vectorstore import search

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/ask", response_model=AskResponse)
def ask(data: AskRequest, current_user: User = Depends(get_current_user)):
    question = data.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    matches = search(question, n_results=3)
    answer = generate_answer(question, matches)

    return AskResponse(question=question, answer=answer, chunks=matches)