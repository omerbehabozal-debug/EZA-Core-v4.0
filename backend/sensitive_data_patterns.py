# -*- coding: utf-8 -*-
"""
sensitive_data_patterns.py – EZA-Core v11.0

Kimlik / TC / telefon tespiti için pattern matching.
"""

import re

SENSITIVE_PATTERNS = [
    r"\bkimlik numaras[ıi]\b",
    r"\btc\s*kimlik\b",
    r"\btc\s*no\b",
    r"\btc\s*kimlik\s*no\b",
    r"\btelefon numaras[ıi]\b",
    r"\biban\b",
    r"\bpasaport\b",
    r"\bpassport\b",
    r"\bnüfus cüzdan[ıi]\b",
    r"\behliyet\s*no\b",
    r"\bkredi kart[ıi]\b",
    r"\bcredit\s*card\b",
    r"\bcvv\b",
    r"\bsecurity\s*code\b",
]


def has_sensitive_data_intent(text: str) -> bool:
    """
    Metinde hassas kişisel veri talebi olup olmadığını kontrol eder.
    
    Args:
        text: Kontrol edilecek metin
        
    Returns:
        True eğer hassas veri talebi tespit edilirse
    """
    t = text.lower()
    return any(re.search(p, t, re.IGNORECASE) for p in SENSITIVE_PATTERNS)

