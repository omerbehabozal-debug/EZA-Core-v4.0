# -*- coding: utf-8 -*-
"""
intent_engine/__init__.py – EZA-IntentEngine v3.0

Modular, computed intent analysis system with:
- Action–Target–Purpose grid
- Per-intent scores and confidence
- Risk fusion (score → level)
- Explicit support for: information, illegal, violence, self-harm, manipulation, sensitive-data, toxicity
"""

from typing import Any, Dict, List

from .lexicon import (
    ACTION_VERBS,
    TARGET_WORDS,
    PURPOSE_CLUES,
    SELF_HARM_KEYWORDS,
    VIOLENCE_KEYWORDS,
    ILLEGAL_KEYWORDS,
    MANIPULATION_KEYWORDS,
    SENSITIVE_DATA_KEYWORDS,
    TOXICITY_KEYWORDS,
    SENSITIVE_DATA_SIGNALS,
)
from .scoring import (
    normalize_text,
    detect_action_hits,
    detect_target_hits,
    detect_purpose_hits,
    compute_intent_scores,
    fuse_risk,
    detect_sensitive_data_hits,
)


def analyze_intent(text: str, language: str = "unknown") -> Dict[str, Any]:
    """
    EZA-IntentEngine v3.0 main function.
    
    Returns comprehensive intent analysis with scores, flags, and metadata.
    """
    # 1) Normalize text
    text_norm = normalize_text(text)
    
    # 2) Compute intent scores
    intent_scores = compute_intent_scores(text_norm)
    
    # 3) Decide primary intent (with tie-breaking order)
    intent_order = [
        "self-harm",
        "violence",
        "illegal",
        "manipulation",
        "sensitive-data",
        "toxicity",
        "information",
    ]
    
    primary = "information"
    max_score = 0.0
    for intent in intent_order:
        score = intent_scores.get(intent, 0.0)
        if score > max_score:
            max_score = score
            primary = intent
    
    # 4) Decide secondary (all categories except primary with score >= 0.4)
    secondary: List[str] = []
    for intent in intent_order:
        if intent != primary and intent_scores.get(intent, 0.0) >= 0.4:
            secondary.append(intent)
    
    # 5) Compute risk_flags, risk_score, risk_level
    risk_flags, risk_score, risk_level = fuse_risk(intent_scores)
    
    # 6) Collect meta info
    action_hits = detect_action_hits(text_norm)
    target_hits = detect_target_hits(text_norm)
    purpose_hits = detect_purpose_hits(text_norm)
    
    # Pattern hits (special patterns like wifi-illegal)
    pattern_hits: List[str] = []
    if any(w in text_norm for w in ["wifi", "wi-fi", "modem"]):
        if any(w in text_norm for w in ["şifre", "sifre", "password", "parola"]):
            if any(w in text_norm for w in ["kır", "kırmak", "kırar", "kirar", "hack", "hacklemek"]):
                pattern_hits.append("wifi-illegal")
    
    # Get sensitive data hits for metadata (Mega Patch v1.0)
    sens_hits = detect_sensitive_data_hits(text_norm)
    
    # Force critical policy when ID number detected (Mega Patch v1.0)
    if sens_hits.get("id_numbers") and len(sens_hits["id_numbers"]) > 0:
        risk_score = 1.0
        risk_level = "critical"
        if "sensitive-data" not in risk_flags:
            risk_flags.append("sensitive-data")
    
    debug_notes = f"Primary: {primary} (score={max_score:.2f}), Risk: {risk_level} ({risk_score:.2f})"
    
    # 7) Return comprehensive dict
    return {
        "primary": primary,
        "secondary": secondary,
        "intent_scores": intent_scores,
        "risk_flags": risk_flags,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "meta": {
            "action_hits": action_hits,
            "target_hits": target_hits,
            "purpose_hits": purpose_hits,
            "pattern_hits": pattern_hits,
            "sens_hits": sens_hits,  # Mega Patch v1.0: sensitive data hits
            "debug_notes": debug_notes,
        },
    }

