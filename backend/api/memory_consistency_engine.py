from typing import Any, Dict, List


class MemoryConsistencyEngine:
    """
    LEVEL 10 – Memory Consistency Engine v1.0

    Görev:
    - Sistem ile kullanıcı arasındaki uzun dönem konuşma kayıtlarında
      tutarlılık analizleri yapmak.
    - 4 temel boyutu değerlendirir:
        policy_consistency, self_contradiction,
        knowledge_drift, user_fact_inconsistency
    """

    def __init__(self) -> None:
        # Rule-based MVP
        self.policy_keywords = ["kural", "sınır", "yasak", "yapamam", "veremem"]
        self.contradiction_keywords = ["ama dün", "daha önce", "çelişiyor", "tutarsız"]
        self.drift_keywords = ["yanlış hatırlıyorsun", "o öyle değildi", "değiştirdin"]
        self.user_fact_keywords = ["sen demiştin", "daha önce söyledin", "bana söyledin"]

    def _normalize(self, text: str) -> str:
        return text.lower()

    def _score(self, text: str, keywords: List[str]) -> float:
        t = self._normalize(text)
        hits = sum(1 for kw in keywords if kw in t)

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
        memory_context: Dict[str, Any] | None,
        model_outputs: Dict[str, Any],
    ) -> Dict[str, Any]:

        try:
            if not memory_context:
                return {
                    "score": 0.0,
                    "level": "low",
                    "dimensions": {
                        "policy_consistency": 0.0,
                        "self_contradiction": 0.0,
                        "knowledge_drift": 0.0,
                        "user_fact_inconsistency": 0.0,
                    },
                    "flags": [],
                    "summary": "Geçmiş hafıza verisi olmadığından tutarsızlık tespit edilmedi.",
                }

            # Metinleri birleştir
            combined = ""

            for msg in memory_context.get("past_user_messages", []):
                combined += f"\nUSER: {msg}"

            for msg in memory_context.get("past_model_messages", []):
                combined += f"\nMODEL: {msg}"

            combined += "\n" + "\n".join(
                v for v in model_outputs.values() if isinstance(v, str)
            )

            # Boyut hesaplamaları
            dims = {
                "policy_consistency": self._score(combined, self.policy_keywords),
                "self_contradiction": self._score(combined, self.contradiction_keywords),
                "knowledge_drift": self._score(combined, self.drift_keywords),
                "user_fact_inconsistency": self._score(combined, self.user_fact_keywords),
            }

            max_dim = max(dims.values())
            avg_dim = sum(dims.values()) / len(dims)
            score = (0.6 * max_dim) + (0.4 * avg_dim)
            level = self._compute_level(score)

            flags = []
            if level in {"high", "critical"}:
                flags.append("memory-inconsistency")
            if dims["knowledge_drift"] >= 0.6:
                flags.append("knowledge-drift")

            risky = [d for d, v in dims.items() if v >= 0.3]

            if not risky:
                summary = "Belirgin bir hafıza tutarsızlığı tespit edilmedi."
            else:
                summary = (
                    f"{', '.join(risky)} boyutlarında tutarsızlık sinyalleri tespit edildi. "
                    f"Genel tutarlılık seviyesi: {level}."
                )

            return {
                "score": round(score, 4),
                "level": level,
                "dimensions": {k: round(v, 4) for k, v in dims.items()},
                "flags": flags,
                "summary": summary,
            }

        except Exception as exc:
            return {
                "score": 0.0,
                "level": "low",
                "dimensions": {
                    "policy_consistency": 0.0,
                    "self_contradiction": 0.0,
                    "knowledge_drift": 0.0,
                    "user_fact_inconsistency": 0.0,
                },
                "flags": ["memory-engine-error"],
                "summary": f"MemoryConsistencyEngine hatası: {exc}",
            }

