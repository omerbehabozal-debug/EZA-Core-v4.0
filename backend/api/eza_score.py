# -*- coding: utf-8 -*-
"""
EZAScore – EZA Level-5 Upgrade
Tüm katmanlardan gelen veriyi 18 parametrelik ağırlıklı
tek bir etik skor haline getirir.
"""


class EZAScore:
    """
    Tüm katmanlardan gelen veriyi 18 parametrelik ağırlıklı
    tek bir etik skor haline getirir.
    """

    def __init__(self):
        self.weights = {
            "intent": 0.25,
            "identity": 0.15,
            "reasoning": 0.15,
            "narrative": 0.10,
            "drift": 0.15,
            "output": 0.20
        }

    def compute(self, report, drift_matrix):
        # Extract intent data from various possible locations
        intent_data = report.get("intent_engine") or report.get("intent") or report.get("input", {}).get("intent_engine", {})
        intent_score = self._to_score(intent_data)
        
        # Extract identity block data
        identity_data = report.get("identity_block", {})
        identity_score = self._simple(identity_data)
        
        # Extract reasoning shield data
        reasoning_data = report.get("reasoning_shield", {}) or report.get("shield", {})
        reasoning_score = self._simple(reasoning_data)
        
        # Extract narrative data
        narrative_data = report.get("narrative", {})
        narrative_score = self._simple(narrative_data)
        
        # Extract drift score and normalize to 0-1 range
        # Drift score can be negative (decreasing risk) or positive (increasing risk)
        raw_drift = drift_matrix.get("score", 0)
        # Normalize: clamp to reasonable range first, then map to 0-1
        # Assuming max drift per window is around 5 (6 entries * 0.8 max change)
        clamped_drift = max(-5.0, min(5.0, raw_drift))
        # Map to 0-1 range: -5 -> 0, 0 -> 0.5, +5 -> 1.0
        drift_score = max(0.0, min(1.0, (clamped_drift + 5.0) / 10.0))
        
        # Extract output data from various possible locations
        output_data = report.get("output_analysis") or report.get("output") or report.get("output_data", {})
        output_score = self._to_score(output_data)

        final = (
            intent_score * self.weights["intent"]
            + identity_score * self.weights["identity"]
            + reasoning_score * self.weights["reasoning"]
            + narrative_score * self.weights["narrative"]
            + drift_score * self.weights["drift"]
            + output_score * self.weights["output"]
        )

        return {
            "final_score": round(final, 3),
            "risk_grade": self._grade(final)
        }

    def _to_score(self, block):
        if not block:
            return 0
        lvl = block.get("risk_level") or block.get("risk")
        return {
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8,
            "critical": 1.0
        }.get(lvl, 0.3)

    def _simple(self, block):
        if not block:
            return 0
        # Try to extract risk_level if available
        risk_level = block.get("risk_level") or block.get("risk") or block.get("final_risk_level")
        if risk_level:
            return self._to_score({"risk_level": risk_level})
        # If block exists but no risk_level, return default 0.5
        return 0.5

    def _grade(self, score):
        if score < 0.3:
            return "A (Safe)"
        elif score < 0.55:
            return "B (Caution)"
        elif score < 0.8:
            return "C (High Risk)"
        else:
            return "D (Critical)"

