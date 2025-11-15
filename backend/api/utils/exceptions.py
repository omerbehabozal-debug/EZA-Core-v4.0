class EZAException(Exception):
    """Genel EZA hata sınıfı."""
    pass


class InvalidInputError(EZAException):
    """Geçersiz kullanıcı girdisi."""
    pass


class LanguageDetectionError(EZAException):
    """Dil tespitinde hata oluştu."""
    pass


class RateLimitExceeded(EZAException):
    """API kullanım limiti aşıldı."""
    pass


class AnalysisFailure(EZAException):
    """Analiz sırasında beklenmeyen hata."""
    pass
