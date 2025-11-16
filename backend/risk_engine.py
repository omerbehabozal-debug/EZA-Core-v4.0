# -*- coding: utf-8 -*-
"""
risk_engine.py – EZA-Core v11.0

Tek merkezli risk + alignment hesabı.
"""

from typing import Dict, Any

from backend.policy_config import RISK_THRESHOLDS, CATEGORY_BASE_WEIGHTS, ALIGNMENT_BASE
from backend.sensitive_data_patterns import has_sensitive_data_intent


def compute_risk_and_alignment(intent_scores: Dict[str, float], raw_text: str) -> Dict[str, Any]:
    """
    IntentEngine v10 çıktısını alıp risk ve alignment hesaplar.
    
    Args:
        intent_scores: IntentEngine çıktısı
            örn: {"illegal": 1.0, "violence": 0, "self-harm": 0, ...}
        raw_text: Orijinal metin (sensitive data kontrolü için)
        
    Returns:
        {
          "primary": "illegal",
          "risk_score": 1.0,
          "risk_level": "critical",
          "alignment_score": 0-100,
          "category": "illegal"
        }
    """
    
    # 1) Sensitive-data override: kimlik vs. tespit edilirse flag ekle
    if has_sensitive_data_intent(raw_text):
        intent_scores = dict(intent_scores)  # kopya
        intent_scores["sensitive-data"] = max(intent_scores.get("sensitive-data", 0), 0.8)
    
    # 2) En yüksek skorlu niyeti bul
    primary = max(intent_scores, key=intent_scores.get)
    primary_score = float(intent_scores[primary])
    
    # 3) Risk seviyesi
    if primary_score >= RISK_THRESHOLDS["critical"]:
        risk_level = "critical"
    elif primary_score >= RISK_THRESHOLDS["high"]:
        risk_level = "high"
    elif primary_score >= RISK_THRESHOLDS["medium"]:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    # 4) EZA Alignment skoru (0–100)
    base = ALIGNMENT_BASE.get(primary, 50)
    # yüksek risk = düşük alignment
    alignment_score = max(0, min(100, base * (1.0 - primary_score)))
    
    return {
        "primary": primary,
        "category": primary,
        "risk_score": round(primary_score, 4),
        "risk_level": risk_level,
        "alignment_score": round(alignment_score, 2),
    }

