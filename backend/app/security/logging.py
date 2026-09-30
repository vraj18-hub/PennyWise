import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Configure structured format for standard logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("pennywise.access")


class AccessLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming HTTP requests, response status, and processing duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        try:
            response: Response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            # Record custom header with processing latency
            response.headers["X-Process-Time-Ms"] = str(duration_ms)

            logger.info(
                f"{client_ip} - {method} {path} -> {response.status_code} ({duration_ms}ms)"
            )
            return response

        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                f"{client_ip} - {method} {path} -> ERROR: {exc} ({duration_ms}ms)"
            )
            raise exc