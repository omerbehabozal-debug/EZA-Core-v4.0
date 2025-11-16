# -*- coding: utf-8 -*-
"""
LEVEL 9 – Abuse & Coercion Engine v1.0
Metinlerde zorbalık, tehdit, baskı, şantaj ve manipülatif "coercion" davranışlarını tespit eden gelişmiş güvenlik katmanı.
"""

from typing import Any, Dict, List


class AbuseEngine:
    """
    LEVEL 9 – Abuse & Coercion Engine v1.0

    Görev:
    - Metinlerde baskı, zorbalık, tehdit, şantaj, manipülasyon ve grooming benzeri kalıpları tespit etmek.
    - 5 boyutta analiz yapar:
        harassment, threat, coercion, blackmail, grooming
    """

    def __init__(self) -> None:
        # Rule-based MVP keyword listeleri
        self.keywords = {
            "harassment": [
                "aptal", "gerizekalı", "salak", "şerefsiz", "mal", "idiot", "stupid", "dumb"
            ],
            "threat": [
                "öldürürüm", "vururum", "mahvederim", "yakacağım", "intikam alırım",
                "kill you", "hurt you", "i will destroy you"
            ],
            "coercion": [
                "zorundasın", "mecbursun", "ya ... ya ...", "yapmazsan", "itaat et",
                "you must", "you have to", "if you don't"
            ],
            "blackmail": [
                "ifşa ederim", "yayarım", "açığa çıkarırım", "rezil ederim",
                "expose you", "leak this", "make it public"
            ],
            "grooming": [
                "kimse seni anlamaz", "sadece ben", "bana güvenmelisin",
                "no one else understands you", "trust only me"
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
            # Model çıktılarını birleştir
            outputs = []
            for key, value in model_outputs.items():
                if isinstance(value, str):
                    outputs.append(value)
                elif isinstance(value, dict) and isinstance(value.get("output_text"), str):
                    outputs.append(value["output_text"])

            combined = input_text + "\n" + "\n".join(outputs)

            # Boyutlar
            dimensions: Dict[str, float] = {}
            for dim_name, kw_list in self.keywords.items():
                dimensions[dim_name] = self._score_dimension(combined, kw_list)

            # Skor
            max_dim = max(dimensions.values()) if dimensions else 0.0
            avg_dim = sum(dimensions.values()) / len(dimensions) if dimensions else 0.0
            score = (0.6 * max_dim) + (0.4 * avg_dim)
            level = self._compute_level(score)

            flags = []
            if level in {"high", "critical"}:
                flags.append("abuse-risk")
            if dimensions.get("threat", 0.0) >= 0.6:
                flags.append("threat")
            if dimensions.get("coercion", 0.0) >= 0.6:
                flags.append("coercion")
            if dimensions.get("blackmail", 0.0) >= 0.6:
                flags.append("blackmail")

            risky_dims = [d for d, v in dimensions.items() if v >= 0.3]
            if not risky_dims:
                summary = "Belirgin bir istismar veya tehdit sinyali tespit edilmedi."
            else:
                summary = (
                    f"{', '.join(risky_dims)} boyutlarında istismar sinyalleri tespit edildi. "
                    f"Genel istismar seviyesi: {level}."
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
                    "harassment": 0.0,
                    "threat": 0.0,
                    "coercion": 0.0,
                    "blackmail": 0.0,
                    "grooming": 0.0,
                },
                "flags": ["abuse-engine-error"],
                "summary": f"AbuseEngine hatası: {exc}",
            }

