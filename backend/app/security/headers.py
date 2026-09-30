from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds standard security headers to every HTTP response."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)

        # Prevent browser from MIME-sniffing response body
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking by forbidding embedding in iframes
        response.headers["X-Frame-Options"] = "DENY"

        # Protect against cross-site scripting
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Only send referrer on same-origin or HTTPS -> HTTPS transitions
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response