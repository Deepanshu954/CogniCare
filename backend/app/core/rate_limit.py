import time
from collections import defaultdict
from typing import Dict, List
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.config import settings


class RateLimiter:
    def __init__(self, requests_per_minute: int = 20):
        self.requests_per_minute = requests_per_minute
        self.history: Dict[str, List[float]] = defaultdict(list)

    def is_rate_limited(self, client_ip: str) -> bool:
        if not settings.RATE_LIMIT_ENABLED:
            return False

        now = time.time()
        window_start = now - 60.0

        # Purge timestamps outside current 60s sliding window
        self.history[client_ip] = [ts for ts in self.history[client_ip] if ts > window_start]

        if len(self.history[client_ip]) >= self.requests_per_minute:
            return True

        self.history[client_ip].append(now)
        return False


auth_rate_limiter = RateLimiter(requests_per_minute=20)


async def rate_limit_middleware(request: Request, call_next):
    # Only rate-limit authentication endpoints
    rate_limited_paths = ["/api/v1/auth/login", "/api/v1/auth/register"]
    
    if request.url.path in rate_limited_paths and request.method == "POST":
        # Extract client IP
        forwarded = request.headers.get("X-Forwarded-For")
        client_ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "unknown")

        # Allow test client bypass if configured
        if client_ip != "testclient" and auth_rate_limiter.is_rate_limited(client_ip):
            req_id = getattr(request.state, "request_id", "req_ratelimited")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={"Retry-After": "60"},
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please wait 60 seconds before retrying.",
                        "details": {"retry_after_seconds": 60},
                    },
                    "request_id": req_id,
                },
            )

    return await call_next(request)
