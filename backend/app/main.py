from fastapi import FastAPI

app = FastAPI(title="PennyWise")

@app.get("/health")
def health():
    return {"status": "ok"}