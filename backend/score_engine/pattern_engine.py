# -*- coding: utf-8 -*-
"""
pattern_engine.py – EZA-SCORE v1.0

Sentence-level pattern detection for advanced risk evaluation.
This layer inspects structure, intent phrases, target relationships and
special red-flag linguistic constructs.

This is intentionally simple for now but fully extensible.
"""

import re
from typing import Dict, List


class PatternEngine:

    # Target patterns (hedef belirten kelimeler)
    TARGET_PATTERNS = [
        r"birini",
        r"birine",
        r"adamı",
        r"kişiyi",
        r"karşıdakini",
        r"hedefi",
    ]

    # Patterns that indicate target-directed hostility
    VIOLENCE_PATTERNS = [
        r"birini.*?öldür",
        r"birine.*?saldır",
        r"kime.*?zarar verebilirim",
        r"nasıl.*?yaralarım",
        r"birini.*?nasıl.*?döv",
        r"nasıl.*?saldır",
        r"birine.*?zarar.*?vermek",
        r"birini.*?öldürmek.*?istiyorum",
        r"birine.*?zarar.*?vermek.*?istiyorum",
        r"nasıl.*?döverim",
        r"nasıl.*?saldırırım",
    ]

    # Patterns for illegal contextual phrasing
    ILLEGAL_PATTERNS = [
        r"başkasının.*?hesab",
        r"komşunun.*?wifi",
        r"başkasına.*?ait.*?şifre",
        r"çalmam lazım",
        r"çalabilir miyim",
    ]

    # Patterns for self-harm contextual phrasing
    SELF_HARM_PATTERNS = [
        r"kendime.*?bir şey yap",
        r"hayatıma.*?son vermek.*?istiyorum",
    ]

    @classmethod
    def match_any(cls, text: str, pattern_list: List[str]) -> bool:
        for p in pattern_list:
            if re.search(p, text, flags=re.IGNORECASE):
                return True
        return False

    @classmethod
    def has_target_pattern(cls, text: str) -> bool:
        """
        Checks if text contains target patterns (birini, birine, etc.)
        """
        return cls.match_any(text, cls.TARGET_PATTERNS)

    @classmethod
    def analyze_patterns(cls, text: str) -> Dict[str, bool]:
        """
        Returns a dict of detected pattern flags.
        """
        return {
            "pattern_violence": cls.match_any(text, cls.VIOLENCE_PATTERNS),
            "pattern_illegal": cls.match_any(text, cls.ILLEGAL_PATTERNS),
            "pattern_self_harm": cls.match_any(text, cls.SELF_HARM_PATTERNS),
            "has_target": cls.has_target_pattern(text),
        }

