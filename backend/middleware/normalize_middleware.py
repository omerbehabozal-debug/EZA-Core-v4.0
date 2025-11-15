from starlette.middleware.base import BaseHTTPMiddleware
from backend.api.utils.normalizer import normalize_text


class NormalizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method == "POST":
            body = await request.body()
            cleaned = normalize_text(body.decode("utf-8"))
            request._body = cleaned.encode("utf-8")
        return await call_next(request)
