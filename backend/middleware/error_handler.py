from fastapi import Request
from fastapi.responses import JSONResponse
from backend.api.utils.exceptions import (
    EZAException,
    InvalidInputError,
    LanguageDetectionError,
    RateLimitExceeded,
    AnalysisFailure,
)
from backend.api.utils.logger import logger


async def eza_exception_handler(request: Request, exc: EZAException):
    logger.error(f"EZAException: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning("Rate limit aşıldı.")
    return JSONResponse(
        status_code=429,
        content={"error": "Çok fazla istek gönderdiniz. Lütfen bekleyin."}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Beklenmeyen hata: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Sunucu hatası. Ekip bilgilendirildi."}
    )
