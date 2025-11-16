# -*- coding: utf-8 -*-
"""
Moral Compass Engine v1.0 – LEVEL 8
Kültürler Arası Etik Değerlendirme
"""

from typing import Any, Dict, List


class MoralCompassEngine:
    """
    LEVEL 8 – Moral Compass Engine v1.0

    Görev:
    - Metni kültürler arası etik boyutlarda analiz eder.
    - 6 ana etik eksen kullanır:
        harm_care, fairness, honesty, autonomy, respect, cultural_sensitivity
    - "low|medium|high|critical" seviyesinde etik risk döndürür.
    """

    def __init__(self) -> None:
        # Rule-based keyword listeleri (MVP)
        self.keywords = {
            "harm_care": [
                "zarar", "öldür", "yarala", "intihar", "tehdit", "acı", "işkence",
                "harm", "kill", "hurt", "violence"
            ],
            "fairness": [
                "ayrımcılık", "haksız", "adaletsiz", "torpil", "eşitsizlik",
                "unfair", "discriminate"
            ],
            "honesty": [
                "yalan", "gizle", "sakla", "dürüst değil", "çarpıt",
                "lie", "deceive", "mislead"
            ],
            "autonomy": [
                "zorla", "mecbur", "şart koş", "baskı", "ikna etme",
                "coerce", "force", "manipulate"
            ],
            "respect": [
                "aşağıla", "hakaret", "küçümse", "onur kırıcı", "saygısız",
                "insult", "humiliate", "offensive"
            ],
            "cultural_sensitivity": [
                "haram", "günah", "kafir", "şeriat", "ibadet", "kutsal",
                "holy", "religion", "sacrilege"
            ],
        }

    def _normalize(self, text: str) -> str:
        return text.lower()

    def _score_dimension(self, text: str, keywords: List[str]) -> float:
        normalized = self._normalize(text)
        hits = sum(1 for kw in keywords if kw in normalized)

        if hits == 0:
            return 0.0
        if hits == 1:
            return 0.25
        if hits == 2:
            return 0.45
        if hits == 3:
            return 0.7
        return 0.9

    def _compute_level(self, score: float) -> str:
        if score >= 0.85:
            return "critical"
        if score >= 0.6:
            return "high"
        if score >= 0.3:
            return "medium"
        return "low"

    def analyze(
        self,
        input_text: str,
        model_outputs: Dict[str, Any],
        intent_engine: Dict[str, Any] | None = None,
        context_graph: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        try:
            outputs = []
            for key, value in model_outputs.items():
                if isinstance(value, str):
                    outputs.append(value)
                elif isinstance(value, dict):
                    if "output_text" in value:
                        outputs.append(value["output_text"])

            combined = input_text + "\n" + "\n".join(outputs)

            dimensions: Dict[str, float] = {}
            for dim_name, kw_list in self.keywords.items():
                dimensions[dim_name] = self._score_dimension(combined, kw_list)

            max_dim = max(dimensions.values()) if dimensions else 0.0
            avg_dim = sum(dimensions.values()) / len(dimensions) if dimensions else 0.0

            score = (0.6 * max_dim) + (0.4 * avg_dim)
            level = self._compute_level(score)

            flags = []
            if level in {"high", "critical"}:
                flags.append("ethical-risk")
            if dimensions.get("cultural_sensitivity", 0.0) >= 0.6:
                flags.append("cultural-sensitive")

            risky_dims = [d for d, v in dimensions.items() if v >= 0.3]
            if not risky_dims:
                summary = "Belirgin bir etik risk sinyali tespit edilmedi."
            else:
                summary = (
                    f"{', '.join(risky_dims)} boyutlarında etik risk sinyalleri bulundu. "
                    f"Genel etik seviye: {level}."
                )

            return {
                "score": round(score, 4),
                "level": level,
                "dimensions": {k: round(v, 4) for k, v in dimensions.items()},
                "flags": flags,
                "summary": summary,
            }
        except Exception as exc:
            return {
                "score": 0.0,
                "level": "low",
                "dimensions": {
                    "harm_care": 0.0,
                    "fairness": 0.0,
                    "honesty": 0.0,
                    "autonomy": 0.0,
                    "respect": 0.0,
                    "cultural_sensitivity": 0.0,
                },
                "flags": ["moral-compass-error"],
                "summary": f"MoralCompassEngine hatası: {exc}",
            }

