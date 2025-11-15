import time
from starlette.middleware.base import BaseHTTPMiddleware

FAIL_THRESHOLD = 5
OPEN_TIME = 10  # saniye


class CircuitBreakerMiddleware(BaseHTTPMiddleware):
    failures = 0
    opened_until = 0

    async def dispatch(self, request, call_next):
        now = time.time()

        # Eğer devre açık ise
        if now < self.opened_until:
            return JSONResponse(
                status_code=503,
                content={"error": "Sistem yoğun. Lütfen sonra tekrar deneyin."},
            )

        try:
            response = await call_next(request)
            self.failures = 0
            return response
        except Exception:
            self.failures += 1
            if self.failures >= FAIL_THRESHOLD:
                self.opened_until = now + OPEN_TIME
            raise
