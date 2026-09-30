import time
from collections import defaultdict, deque
from fastapi import HTTPException, Request, status


class SlidingWindowRateLimiter:
    """In-memory sliding window rate limiter per client IP."""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Maps client IP -> deque of request timestamps
        self.clients: dict[str, deque] = defaultdict(deque)

    async def __call__(self, request: Request):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.window_seconds

        timestamps = self.clients[client_ip]

        # 1. Evict timestamps outside the current sliding window
        while timestamps and timestamps[0] < window_start:
            timestamps.popleft()

        # 2. Check if the client exceeded the allowed rate
        if len(timestamps) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - timestamps[0])) + 1
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )

        # 3. Record current request timestamp
        timestamps.append(now)


# Pre-configured rate limiting dependencies:
# Strict for Auth: 5 attempts per 60 seconds (prevents brute-force attacks)
auth_rate_limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=60)

# Moderate for LLM generation: 10 queries per 60 seconds (protects local LLM compute)
llm_rate_limiter = SlidingWindowRateLimiter(max_requests=10, window_seconds=60)
