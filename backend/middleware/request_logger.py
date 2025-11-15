from starlette.middleware.base import BaseHTTPMiddleware
from backend.api.utils.logger import logger


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"[REQUEST] {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"[RESPONSE] {response.status_code} {request.url}")
        return response
