from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class RetrievedChunk(BaseModel):
    text: str
    source: str
    distance: float


class AskResponse(BaseModel):
    question: str
    answer: str
    chunks: list[RetrievedChunk]