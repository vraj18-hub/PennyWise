import io

import pandas as pd
from sqlalchemy.orm import Session

from app.db.models import Transaction

REQUIRED_COLUMNS = {"date", "description", "amount", "category"}


def parse_csv(file_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(file_bytes))
    df.columns = [c.strip().lower() for c in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {', '.join(missing)}")

    return df


def save_transactions(db: Session, user_id: int, df: pd.DataFrame) -> tuple[int, int]:
    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            transaction = Transaction(
                user_id=user_id,
                date=pd.to_datetime(row["date"]),
                description=str(row["description"])[:255],
                amount=float(row["amount"]),
                category=str(row["category"]).strip().lower()[:50],
            )
            db.add(transaction)
            inserted += 1
        except (ValueError, TypeError):
            skipped += 1

    db.commit()
    return inserted, skipped

def compute_summary(db: Session, user_id: int) -> dict:
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    rows = [
        {"amount": float(t.amount), "category": t.category}
        for t in query.all()
    ]

    if not rows:
        return {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "savings_rate": 0.0,
            "by_category": [],
        }

    df = pd.DataFrame(rows)

    income_mask = df["amount"] > 0
    total_income = round(df.loc[income_mask, "amount"].sum(), 2)
    total_expenses = round(-df.loc[~income_mask, "amount"].sum(), 2)

    savings_rate = 0.0
    if total_income > 0:
        savings_rate = round((total_income - total_expenses) / total_income * 100, 2)

    expenses_df = df.loc[~income_mask].copy()
    expenses_df["amount"] = -expenses_df["amount"]
    by_category = (
        expenses_df.groupby("category")["amount"]
        .sum()
        .round(2)
        .reset_index()
        .rename(columns={"amount": "total"})
        .to_dict(orient="records")
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings_rate": savings_rate,
        "by_category": by_category,
    }