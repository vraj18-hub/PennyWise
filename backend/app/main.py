import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.analytics.router import router as analytics_router
from app.auth.router import router as auth_router
from app.db import models  # noqa: F401
from app.db.database import Base, engine
from app.insights.router import router as insights_router
from app.rag.router import router as rag_router
from app.security.headers import SecurityHeadersMiddleware
from app.security.logging import AccessLoggingMiddleware

error_logger = logging.getLogger("pennywise.errors")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PennyWise")

# 1. Standard HTTP Security Headers
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AccessLoggingMiddleware)

# 2. Strict CORS policy
ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://vraj18-hub.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# 3. Global Safe Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catches unexpected exceptions, logs traceback internally, returns safe JSON."""
    error_logger.exception(
        f"Unhandled server error at {request.method} {request.url.path}: {exc}"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected server error occurred. Our team has been notified.",
        },
    )

app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(rag_router)
app.include_router(insights_router)


@app.get("/health")
def health():
    return {"status": "ok"}
