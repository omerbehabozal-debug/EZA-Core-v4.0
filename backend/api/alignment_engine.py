# -*- coding: utf-8 -*-
"""
alignment_engine.py – EZA-Core v5
Input ve output analizlerini birleştirip etik uyum (alignment) skoru üretir.
"""

from typing import Any, Dict, List

from data_store.event_logger import log_event


def _get_max_risk(risk_in: float, risk_out: float) -> float:
    return max(risk_in, risk_out)


def _risk_to_label(score: float, has_critical_flag: bool) -> str:
    if has_critical_flag:
        return "Critical"
    if score >= 0.8:
        return "Unsafe"
    if score >= 0.4:
        return "Caution"
    return "Safe"


def compute_alignment(
    input_analysis: Dict[str, Any],
    output_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    EZA-Core v5 Alignment Hesabı.

    - Intent / risk / duygu bazında input-output uyumunu hesaplar.
    - Hem sayısal skor hem de "Safe / Caution / Unsafe / Critical" etiketi üretir.
    """
    try:
        ia_ok = input_analysis.get("ok", False)
        oa_ok = output_analysis.get("ok", False)

        if not (ia_ok and oa_ok):
            result = {
                "alignment": "Unknown",
                "alignment_score": 0.0,
                "verdict": "Unknown",
                "details": {
                    "reason": "Input veya output analizi başarısız.",
                },
            }
            log_event("alignment_computed", result)
            return result

        in_risk_score = float(input_analysis.get("risk_score", 0.0))
        out_risk_score = float(output_analysis.get("risk_score", 0.0))

        in_flags: List[str] = input_analysis.get("risk_flags", []) or []
        out_flags: List[str] = output_analysis.get("risk_flags", []) or []

        # Risk bayraklarını daha doğru birleştir (input illegal ise output da illegal sayılır)
        all_flags = list(set(in_flags + out_flags))
        if "illegal" in in_flags:
            if "illegal" not in all_flags:
                all_flags.append("illegal")

        has_self_harm = "self-harm" in all_flags
        has_critical_flag = has_self_harm or "violence" in all_flags or "illegal" in all_flags

        max_risk = _get_max_risk(in_risk_score, out_risk_score)

        # Basit ama açıklanabilir skor: 1 - max_risk
        alignment_score = max(0.0, 1.0 - max_risk)
        verdict = _risk_to_label(max_risk, has_critical_flag)

        details: Dict[str, Any] = {
            "input_risk_score": in_risk_score,
            "output_risk_score": out_risk_score,
            "risk_flags": all_flags,
        }

        # Self-harm durumunda özel etiket
        if has_self_harm:
            details["note"] = "Self-harm riski algılandı. Yanıtlar son derece dikkatli olmalı."

        result = {
            "alignment": verdict,
            "alignment_score": alignment_score,
            "verdict": verdict,
            "details": details,
        }

        log_event("alignment_computed", result)
        return result

    except Exception as e:  # noqa: BLE001
        result = {
            "alignment": "Error",
            "alignment_score": 0.0,
            "verdict": "Error",
            "details": {"error": str(e)},
        }
        log_event("alignment_error", result)
        return result
