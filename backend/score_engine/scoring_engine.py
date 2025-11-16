# -*- coding: utf-8 -*-
"""
scoring_engine.py – EZA-SCORE v1.0

Advanced weighted scoring engine with:
- Multi-hit scoring
- Category interactions
- Escalation multipliers
- Pattern-based risk escalation
"""

from typing import Dict, List
from backend.score_engine.pattern_engine import PatternEngine


class EzaScoringEngine:

    # Base risk weights
    BASE_WEIGHTS = {
        "self-harm": 1.00,
        "violence": 0.90,
        "illegal": 0.85,
        "manipulation": 0.75,
        "sensitive-data": 0.70,
        "toxicity": 0.65,
    }

    # Category interaction multipliers
    INTERACTION_MATRIX = {
        ("illegal", "manipulation"): 1.10,
        ("violence", "toxicity"): 1.08,
        ("self-harm", "toxicity"): 1.05,
        ("illegal", "sensitive-data"): 1.07,
    }

    @classmethod
    def compute_score(cls, categories: List[str], text: str) -> float:
        """
        Multi-hit risk calculation with interaction logic
        and pattern-based escalation.
        """

        if not categories:
            return 0.0

        # Step 1: Base risk accumulation
        base_scores = [cls.BASE_WEIGHTS.get(cat, 0.0) for cat in categories]
        score = max(base_scores)

        # Step 2: Interaction escalation
        for (c1, c2), multiplier in cls.INTERACTION_MATRIX.items():
            if c1 in categories and c2 in categories:
                score *= multiplier

        # Step 3: Pattern analysis
        patterns = PatternEngine.analyze_patterns(text)
        if patterns["pattern_illegal"]:
            score = max(score, 0.92)
        if patterns["pattern_violence"]:
            score = max(score, 0.95)
        if patterns["pattern_self_harm"]:
            score = 1.00

        # Cap limit
        return min(score, 1.00)

    @staticmethod
    def classify_risk_level(score: float) -> str:
        if score >= 0.90:
            return "critical"
        if score >= 0.70:
            return "high"
        if score >= 0.40:
            return "medium"
        return "low"

