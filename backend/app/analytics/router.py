from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.analytics.schemas import SpendingSummary, UploadResult
from app.analytics.service import compute_summary, parse_csv, save_transactions
from app.analytics.schemas import UploadResult
from app.analytics.service import parse_csv, save_transactions
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import User

router = APIRouter(prefix="/transactions", tags=["transactions"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/upload", response_model=UploadResult)
async def upload_transactions(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are accepted")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    try:
        df = parse_csv(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    inserted, skipped = save_transactions(db, current_user.id, df)
    return UploadResult(inserted=inserted, skipped=skipped)

@router.get("/summary", response_model=SpendingSummary)
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    summary = compute_summary(db, current_user.id)
    return summary

