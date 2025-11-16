# -*- coding: utf-8 -*-
"""
output_analyzer.py – EZA-Core v5
Model çıktısını kalite, güvenlik ve risk açısından analiz eder.
"""

from typing import Any, Dict, List

from data_store.event_logger import log_event

from .input_analyzer import (
    compute_risk_flags,
    detect_emotional_tone,
)


def _base_analysis(text: str) -> Dict[str, Any]:
    """
    Ortak analiz fonksiyonu – input ile benzer risk motorunu kullanır.
    """
    risk_info = compute_risk_flags(text)
    emotional_tone = detect_emotional_tone(text)

    risk_flags = risk_info["risk_flags"]
    risk_score = risk_info["risk_score"]

    risk_level = "low"
    if risk_score >= 0.9:
        risk_level = "critical"
    elif risk_score >= 0.7:
        risk_level = "high"
    elif risk_score >= 0.4:
        risk_level = "medium"

    safety_issues: List[str] = risk_flags.copy()

    analysis = {
        "quality_score": 85,
        "helpfulness": "Model çıktısı genel olarak anlaşılır.",
        "safety_issues": safety_issues,
        "policy_violations": [],
        "summary": "Çıktı analizi tamamlandı.",
    }

    return {
        "risk_flags": risk_flags,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "emotional_tone": emotional_tone,
        "analysis": analysis,
    }


def analyze_output(output_text: str, model: str = "chatgpt") -> Dict[str, Any]:
    """
    Model çıktısının etik / güvenlik analizi.
    """
    try:
        base = _base_analysis(output_text)

        result = {
            "ok": True,
            "model": model,
            "output_text": output_text,
            "risk_flags": base["risk_flags"],
            "risk_score": base["risk_score"],
            "risk_level": base["risk_level"],
            "emotional_tone": base["emotional_tone"],
            "analysis": base["analysis"],
            "error": None,
        }

        # Input riskleri output analizine yansıt (özellikle illegal / violence durumları)
        try:
            # Global input analizini yakala (sadece EZA-Core içinde çalışır)
            from backend.api.input_analyzer import compute_risk_flags
            input_risks = compute_risk_flags(output_text)
            merged_flags = list(set(result["risk_flags"] + input_risks.get("risk_flags", [])))
            result["risk_flags"] = merged_flags

            # Illegal içerik varsa risk seviyesi yükselsin
            if "illegal" in merged_flags:
                result["risk_score"] = max(result["risk_score"], 0.85)
                result["risk_level"] = "high"
        except Exception:
            pass

        log_event("output_analyzed", result)
        return result

    except Exception as e:  # noqa: BLE001
        err = {
            "ok": False,
            "model": model,
            "output_text": output_text,
            "analysis": {},
            "error": str(e),
        }
        log_event("output_analysis_error", err)
        return err


def evaluate_output(output_text: str) -> Dict[str, Any]:
    """
    /pair endpoint'i için sade skor döndürür.
    """
    result = analyze_output(output_text, model="pair-eval")
    # Alignment motoru bu alanları kullanacak, burada yapı bozulmasın.
    return result
