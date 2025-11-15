from langdetect import detect
from .exceptions import LanguageDetectionError


def detect_language_safe(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        raise LanguageDetectionError("Dil tespit edilemedi.")
