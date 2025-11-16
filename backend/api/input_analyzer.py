# -*- coding: utf-8 -*-
"""
input_analyzer.py – EZA-Core v10 + EZA-IntentEngine v3.0

Fully level-3 professional analysis system with modular Intent Engine:
- EZA-IntentEngine v3.0 (Action–Target–Purpose grid)
- Per-intent scores and confidence
- Risk fusion (score → level)
- Level-3 patches: Violence, Manipulation, Wifi-Illegal, Toxicity Fix
"""

from typing import Any, Dict, List
import re

from backend.intent_engine import analyze_intent as intent_engine_analyze
from data_store.event_logger import log_event


# Intent engine handles all lexicon and scoring internally


def detect_language(text: str) -> str:
    """
    Enhanced language detector for Turkish.
    Checks Turkish-specific characters and stopwords.
    """
    t = text.lower()
    
    # Check for Turkish-specific characters
    turkish_chars = ["ğ", "ü", "ş", "ö", "ç", "ı", "İ", "Ğ", "Ü", "Ş", "Ö", "Ç"]
    if any(char in text for char in turkish_chars):
        return "tr"
    
    # Check for Turkish stopwords
    turkish_stopwords = [
        "birini", "nasıl", "nasil", "arkadaş", "kandır", "döver",
        "şifre", "sifre", "birine", "kandırmak", "kandir", "arkadaşımı",
        "kararlarını", "etkilemek", "istiyorum", "kırarım", "kirar"
    ]
    if any(stopword in t for stopword in turkish_stopwords):
        return "tr"
    
    # Fallback to English
    if re.search(r"[a-z]", t):
        return "en"
    
    return "unknown"


def detect_emotional_tone(text: str) -> str:
    """
    Simple emotional tone detection.
    """
    t = text.lower()
    if any(w in t for w in ["korkuyorum", "endişeliyim", "kaygılı"]):
        return "anxious"
    if any(w in t for w in ["üzgünüm", "mutsuzum", "yalnızım"]):
        return "sad"
    if any(w in t for w in ["sinirliyim", "öfkeliyim"]):
        return "angry"
    if any(w in t for w in ["mutluyum", "harika"]):
        return "positive"
    return "neutral"


def analyze_input(text: str) -> Dict[str, Any]:
    """
    EZA-Core v10 input analyzer using EZA-IntentEngine v3.0.
    """
    try:
        if not text.strip():
            raise ValueError("Boş metin analiz edilemez.")

        # Detect language
        language = detect_language(text)
        
        # Use Intent Engine v3.0
        intent_result = intent_engine_analyze(text=text, language=language)
        
        # Extract intent structure
        intent = {
            "primary": intent_result.get("primary", "information"),
            "secondary": intent_result.get("secondary", []),
        }
        
        # Extract risk information
        risk_flags = intent_result.get("risk_flags", [])
        risk_score = float(intent_result.get("risk_score", 0.0))
        risk_level = intent_result.get("risk_level", "low")
        
        # Emotional tone
        tone = detect_emotional_tone(text)
        
        # Analysis dict
        analysis = {
            "quality_score": 85,
            "helpfulness": "EZA-IntentEngine v3.0 – çok katmanlı niyet ve risk analizi tamamlandı.",
            "safety_issues": risk_flags,
            "policy_violations": [],
            "summary": "Level-3 intent engine: action–target–purpose + weighted matrix.",
        }

        result = {
            "ok": True,
            "model": "eza-input-v10",
            "raw_text": text,
            "language": language,
            "intent": intent,
            "emotional_tone": tone,
            "risk_flags": risk_flags,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "analysis": analysis,
            "error": None,
            # Optional: include full intent engine result for debugging
            "intent_engine": intent_result,
        }

        log_event("input_analyzed_v10", result)
        return result

    except Exception as e:  # noqa: BLE001
        err = {
            "ok": False,
            "model": "eza-input-v10",
            "raw_text": text,
            "analysis": {},
            "error": str(e),
        }
        log_event("input_analysis_error_v10", err)
        return err
