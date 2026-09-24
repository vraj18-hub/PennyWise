from pydantic import BaseModel


class InsightRequest(BaseModel):
    question: str


class InsightResponse(BaseModel):
    question: str
    answer: str