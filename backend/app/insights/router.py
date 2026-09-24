from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.insights.schemas import InsightRequest, InsightResponse
from app.insights.service import generate_insight

router = APIRouter(prefix="/insights", tags=["insights"])


@router.post("/ask", response_model=InsightResponse)
def ask_insight(
    data: InsightRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    question = data.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer = generate_insight(db, current_user.id, question)

    return InsightResponse(question=question, answer=answer)