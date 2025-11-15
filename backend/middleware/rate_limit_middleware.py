from starlette.middleware.base import BaseHTTPMiddleware
from backend.api.utils.rate_limiter import rate_limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        user_id = request.client.host  # IP bazlı
        rate_limiter.check(user_id)
        return await call_next(request)
