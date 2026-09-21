from fastapi import FastAPI

from app.db.database import Base, engine
from app.db import models  # noqa: F401  (needed so Base knows about User)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PennyWise")


@app.get("/health")
def health():
    return {"status": "ok"}