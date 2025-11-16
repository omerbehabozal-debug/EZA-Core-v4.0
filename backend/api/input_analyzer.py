# -*- coding: utf-8 -*-
"""
input_analyzer.py – EZA-Core v5 (wifi + illegal patch)

Kullanıcı girdisini niyet, risk ve duygu düzeyinde analiz eden katman.

"""

from typing import Any, Dict, List

import re

from data_store.event_logger import log_event

SELF_HARM_KEYWORDS = [
    "intihar",
    "kendimi öldürmek",
    "hayatıma son vermek",
    "yaşamak istemiyorum",
    "yaşamak istemem",
    "ölmek istiyorum",
]

VIOLENCE_KEYWORDS = [
    "öldürmek",
    "vurmak",
    "bıçaklamak",
    "saldırmak",
    "döv",
    "yaralamak",
]

ILLEGAL_KEYWORDS = [
    "hack",
    "hacker",
    "hacklemek",
    "kart kopyalama",
    "kredi kartı dolandırıcılığı",
    "banka hack",
    "banka hesabı hack",
    "hesap hack",
    "hesap çalma",
    "bomba yapmak",
    "uyuşturucu",
]

MANIPULATION_KEYWORDS = [
    "manipüle et",
    "kandır",
    "psikolojik baskı",
    "zihinsel oyun",
]

SENSITIVE_DATA_KEYWORDS = [
    "tc kimlik",
    "t.c. kimlik",
    "kimlik numarası",
    "şifre",
    "sifre",
    "parola",
    "iban",
]

TOXICITY_KEYWORDS = [
    "ırkçı",
    "nefret",
    "geri zekalı",
    "aptal",
    "salak",
]


def detect_language(text: str) -> str:
    """Çok basit bir dil tespiti – sadece demo için."""
    text_lower = text.lower()
    if re.search(r"[ığüşöçİĞÜŞÖÇ]", text_lower):
        return "tr"
    if re.search(r"[a-z]", text_lower):
        return "en"
    return "unknown"


def _is_wifi_illegal(text_lower: str) -> bool:
    """
    Wifi şifresi kırma gibi açıkça illegal olan durumları yakalar.
    Yazım hatalarına toleranslıdır.
    """
    t = text_lower
    if "wifi" in t and any(w in t for w in ["şifre", "sifre", "password"]):
        if any(w in t for w in ["kır", "kir", "kırmak", "kırar", "kırarım", "kırarim", "kırma", "kirma", "hack"]):
            return True
    return False


def classify_intent(text: str) -> Dict[str, Any]:
    """
    Kullanıcının niyetini kaba taslak sınıflandır.
    """
    t = text.lower()

    primary = "information"
    secondary: List[str] = []

    wifi_illegal = _is_wifi_illegal(t)

    if any(w in t for w in SELF_HARM_KEYWORDS):
        primary = "self-harm"
    elif wifi_illegal or any(w in t for w in ILLEGAL_KEYWORDS):
        primary = "illegal"
    elif any(w in t for w in VIOLENCE_KEYWORDS):
        primary = "violence"
    elif any(w in t for w in MANIPULATION_KEYWORDS):
        primary = "manipulation"

    if any(w in t for w in SENSITIVE_DATA_KEYWORDS):
        secondary.append("sensitive-data")
    if any(w in t for w in TOXICITY_KEYWORDS):
        secondary.append("toxicity")

    return {
        "primary": primary,
        "secondary": secondary,
    }


def detect_emotional_tone(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["korkuyorum", "endişeliyim", "kaygılıyım", "panik"]):
        return "anxious"
    if any(w in t for w in ["çok üzgünüm", "mutsuzum", "depresif", "yalnızım"]):
        return "sad"
    if any(w in t for w in ["sinirliyim", "öfkeliyim", "çok kızgınım"]):
        return "angry"
    if any(w in t for w in ["heyecanlıyım", "mutluyum", "harika hissediyorum"]):
        return "positive"
    return "neutral"


def compute_risk_flags(text: str) -> Dict[str, Any]:
    t = text.lower()
    flags: List[str] = []
    score = 0.0

    # 1) Wifi şifresi kırma – açık illegal durum
    if _is_wifi_illegal(t):
        if "illegal" not in flags:
            flags.append("illegal")
        score = max(score, 0.85)

    # 2) Standart risk listeleri

    # Self-harm
    if any(w in t for w in SELF_HARM_KEYWORDS):
        if "self-harm" not in flags:
            flags.append("self-harm")
        score = max(score, 1.0)

    # Violence
    if any(w in t for w in VIOLENCE_KEYWORDS):
        if "violence" not in flags:
            flags.append("violence")
        score = max(score, 0.9)

    # Illegal (genel)
    if any(w in t for w in ILLEGAL_KEYWORDS):
        if "illegal" not in flags:
            flags.append("illegal")
        score = max(score, 0.85)

    # Manipulation
    if any(w in t for w in MANIPULATION_KEYWORDS):
        if "manipulation" not in flags:
            flags.append("manipulation")
        score = max(score, 0.75)

    # Sensitive-data
    if any(w in t for w in SENSITIVE_DATA_KEYWORDS):
        if "sensitive-data" not in flags:
            flags.append("sensitive-data")
        score = max(score, 0.7)

    # Toxicity
    if any(w in t for w in TOXICITY_KEYWORDS):
        if "toxicity" not in flags:
            flags.append("toxicity")
        score = max(score, 0.65)

    return {
        "risk_flags": flags,
        "risk_score": score,
    }


def analyze_input(text: str) -> Dict[str, Any]:
    """
    EZA-Core v5 input analizi.
    """
    try:
        if not text or not text.strip():
            raise ValueError("Boş metin analiz edilemez.")

        language = detect_language(text)
        intent = classify_intent(text)
        emotional_tone = detect_emotional_tone(text)
        risk_info = compute_risk_flags(text)

        risk_flags = risk_info["risk_flags"]
        risk_score = risk_info["risk_score"]

        risk_level = "low"
        if risk_score >= 0.9:
            risk_level = "critical"
        elif risk_score >= 0.7:
            risk_level = "high"
        elif risk_score >= 0.4:
            risk_level = "medium"

        analysis = {
            "quality_score": 80,
            "helpfulness": "EZA v5 – Input analizi (wifi + illegal patch aktif).",
            "safety_issues": risk_flags,
            "policy_violations": [],
            "summary": "EZA v5 – Niyet, risk ve duygu analizi tamamlandı.",
        }

        result = {
            "ok": True,
            "model": "eza-input-v5",
            "raw_text": text,
            "language": language,
            "intent": intent,
            "emotional_tone": emotional_tone,
            "risk_flags": risk_flags,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "analysis": analysis,
            "error": None,
        }

        log_event("input_analyzed", result)
        return result

    except Exception as e:  # noqa: BLE001
        err = {
            "ok": False,
            "model": "eza-input-v5",
            "raw_text": text,
            "analysis": {},
            "error": str(e),
        }
        log_event("input_analysis_error", err)
        return err
