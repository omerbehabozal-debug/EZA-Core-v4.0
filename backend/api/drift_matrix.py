# -*- coding: utf-8 -*-
"""
DriftMatrix – EZA Level-5 Upgrade
Risk davranışının zaman içinde artış/azalış eğrisini hesaplar.
Multi-turn memory üzerinden risk momentum analizi üretir.
"""


class DriftMatrix:
    """
    Risk davranışının zaman içinde artış/azalış eğrisini hesaplar.
    Multi-turn memory üzerinden risk momentum analizi üretir.
    """

    def __init__(self, window=6):
        self.window = window

    def compute(self, memory):
        """
        memory: [{'user': '...', 'model': '...'}]
        her entry için input-output risk ortalaması hesaplanır.
        """
        if not memory or len(memory) < 2:
            return {
                "trend": "stable",
                "changes": [],
                "score": 0
            }

        changes = []
        prev = None
        
        # Risk data parsing
        for item in memory[-self.window:]:
            if "report" in item and "risk_level" in item["report"]:
                current = self._risk_to_num(item["report"]["risk_level"])
                if prev is not None:
                    diff = current - prev
                    changes.append(diff)
                prev = current

        if not changes:
            trend = "stable"
            score = 0
        else:
            score = sum(changes)
            if score > 0.5:
                trend = "increasing-risk"
            elif score < -0.5:
                trend = "decreasing-risk"
            else:
                trend = "stable"

        return {
            "trend": trend,
            "changes": changes,
            "score": score
        }

    def _risk_to_num(self, level):
        mapping = {
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8,
            "critical": 1.0
        }
        return mapping.get(level, 0.2)

