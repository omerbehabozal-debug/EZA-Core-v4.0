# -*- coding: utf-8 -*-
"""
intent_engine/scoring.py – EZA-IntentEngine v3.0

Scoring functions for intent analysis: normalization, hit detection, score computation, risk fusion.
"""

from typing import Any, Dict, List, Tuple

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

# Weight constants
W_ACTION = 0.4
W_TARGET = 0.3
W_PURPOSE = 0.3

# Risk thresholds
THRESHOLD_SELF_HARM = 0.6
THRESHOLD_VIOLENCE = 0.6
THRESHOLD_ILLEGAL = 0.6
THRESHOLD_MANIPULATION = 0.6
THRESHOLD_SENSITIVE_DATA = 0.6
THRESHOLD_TOXICITY = 0.6


def normalize_text(text: str) -> str:
    """
    Normalize text: lowercase, strip, basic Turkish char normalization.
    """
    if not text:
        return ""
    
    # Lowercase and strip
    normalized = text.lower().strip()
    
    # Basic Turkish char normalization (optional, but helpful)
    # ö/ó → o (in some contexts), but we'll keep Turkish chars for now
    # Just ensure consistent lowercase
    
    return normalized


def detect_action_hits(text: str) -> Dict[str, Dict[str, Any]]:
    """
    Detect action verb hits in text.
    Returns dict with count and tokens for each category.
    """
    hits: Dict[str, Dict[str, Any]] = {}
    
    for category, verbs in ACTION_VERBS.items():
        tokens: List[str] = []
        for verb in verbs:
            if verb in text:
                tokens.append(verb)
        
        hits[category] = {
            "count": len(tokens),
            "tokens": tokens,
        }
    
    return hits


def detect_target_hits(text: str) -> Dict[str, Dict[str, Any]]:
    """
    Detect target word hits in text.
    """
    hits: Dict[str, Dict[str, Any]] = {}
    
    for category, words in TARGET_WORDS.items():
        tokens: List[str] = []
        for word in words:
            if word in text:
                tokens.append(word)
        
        hits[category] = {
            "count": len(tokens),
            "tokens": tokens,
        }
    
    return hits


def detect_purpose_hits(text: str) -> Dict[str, Dict[str, Any]]:
    """
    Detect purpose clue hits in text.
    """
    hits: Dict[str, Dict[str, Any]] = {}
    
    for category, clues in PURPOSE_CLUES.items():
        tokens: List[str] = []
        for clue in clues:
            if clue in text:
                tokens.append(clue)
        
        hits[category] = {
            "count": len(tokens),
            "tokens": tokens,
        }
    
    return hits


def detect_sensitive_data_hits(text: str) -> Dict[str, List[str]]:
    """
    Helper function to detect sensitive data hits for metadata.
    Returns the sd_hits dictionary.
    """
    sd_hits: Dict[str, List[str]] = {
        "id_numbers": [],
        "personal_identifiers": [],
        "relational_targets": [],
        "lookup_patterns": []
    }
    
    # Scan each category
    for category, items in SENSITIVE_DATA_SIGNALS.items():
        for item in items:
            if item in text:
                sd_hits[category].append(item)
    
    return sd_hits


def compute_intent_scores(text: str) -> Dict[str, float]:
    """
    Compute per-intent scores based on action/target/purpose hits and special patterns.
    """
    scores: Dict[str, float] = {
        "information": 0.0,
        "illegal": 0.0,
        "violence": 0.0,
        "self-harm": 0.0,
        "manipulation": 0.0,
        "sensitive-data": 0.0,
        "toxicity": 0.0,
    }
    
    # Get hits
    action_hits = detect_action_hits(text)
    target_hits = detect_target_hits(text)
    purpose_hits = detect_purpose_hits(text)
    
    # Self-harm: special rule (highest priority)
    if any(keyword in text for keyword in SELF_HARM_KEYWORDS):
        scores["self-harm"] = 1.0
    
    # Violence: action + target boost
    violence_action_count = action_hits.get("violence", {}).get("count", 0)
    has_other_person_target = target_hits.get("other_person", {}).get("count", 0) > 0
    
    # Check violence keywords directly first (highest priority)
    if any(keyword in text for keyword in VIOLENCE_KEYWORDS):
        scores["violence"] = 0.9
        if has_other_person_target:
            scores["violence"] = 0.95
    elif violence_action_count > 0:
        scores["violence"] = min(0.9 + (violence_action_count * 0.1), 1.0)
        if has_other_person_target:
            scores["violence"] = min(scores["violence"] + 0.1, 1.0)
    
    # Wifi-illegal pattern (special case)
    wifi_terms = ["wifi", "wi-fi", "modem"]
    password_terms = ["şifre", "sifre", "password", "parola"]
    crack_terms = ["kır", "kırmak", "kırar", "kırarım", "kırarim", "kirar", "kirma", "kirmak", "hack", "hacklemek"]
    
    has_wifi = any(w in text for w in wifi_terms)
    has_password = any(w in text for w in password_terms)
    has_crack = any(w in text for w in crack_terms)
    
    if has_wifi and has_password and has_crack:
        scores["illegal"] = 0.9
        scores["sensitive-data"] = 0.7
    
    # Illegal: action + target boost
    illegal_action_count = action_hits.get("illegal", {}).get("count", 0)
    has_system_target = target_hits.get("system", {}).get("count", 0) > 0
    
    if illegal_action_count > 0:
        scores["illegal"] = max(scores["illegal"], min(0.85 + (illegal_action_count * 0.1), 1.0))
        if has_system_target:
            scores["illegal"] = min(scores["illegal"] + 0.1, 1.0)
    
    # Check illegal keywords directly
    if any(keyword in text for keyword in ILLEGAL_KEYWORDS):
        scores["illegal"] = max(scores["illegal"], 0.85)
    
    # Manipulation: check pattern first (manipulation verb + target)
    manipulation_verbs = ["kandır", "kandir", "kandırmak", "kandirmak", "etkilemek", "yönlendirmek"]
    manip_targets = ["birini", "birine", "arkadaşımı", "arkadasimi", "kararlarını", "arkadaşımın"]
    
    has_manip_verb = any(verb in text for verb in manipulation_verbs)
    has_manip_target = any(target in text for target in manip_targets)
    
    if has_manip_verb and has_manip_target:
        scores["manipulation"] = 0.75
    elif has_manip_verb:
        scores["manipulation"] = 0.7
    
    # Check manipulation keywords directly
    if any(keyword in text for keyword in MANIPULATION_KEYWORDS):
        scores["manipulation"] = max(scores["manipulation"], 0.75)
    
    # Action + target + purpose boost
    manipulation_action_count = action_hits.get("manipulation", {}).get("count", 0)
    has_other_person_target = target_hits.get("other_person", {}).get("count", 0) > 0
    has_hidden_purpose = purpose_hits.get("hidden", {}).get("count", 0) > 0
    
    if manipulation_action_count > 0:
        scores["manipulation"] = max(scores["manipulation"], min(0.75 + (manipulation_action_count * 0.1), 1.0))
        if has_other_person_target:
            scores["manipulation"] = min(scores["manipulation"] + 0.1, 1.0)
        if has_hidden_purpose:
            scores["manipulation"] = min(scores["manipulation"] + 0.1, 1.0)
    
    # Sensitive-data: Level-3 Mega Patch v1.0 - Enhanced detection
    # Use new sensitive_data_signals with weighted scoring
    sd_hits = detect_sensitive_data_hits(text)
    
    # Scoring logic with weights
    sens_score = 0.0
    weight = {
        "id_numbers": 0.60,
        "personal_identifiers": 0.40,
        "relational_targets": 0.25,
        "lookup_patterns": 0.35
    }
    
    for cat, hits in sd_hits.items():
        if hits:
            sens_score += len(hits) * weight[cat]
    
    # Cap at critical threshold
    sens_score = min(sens_score, 1.0)
    
    # Strong rule: ID numbers always critical
    if sd_hits["id_numbers"]:
        sens_score = 1.0  # always critical
    
    # Set sensitive-data score
    if sens_score > 0:
        scores["sensitive-data"] = sens_score
    # Fallback to old keyword-based detection
    elif any(keyword in text for keyword in SENSITIVE_DATA_KEYWORDS):
        scores["sensitive-data"] = 0.7
    
    # Toxicity: only explicit insults
    if any(keyword in text for keyword in TOXICITY_KEYWORDS):
        scores["toxicity"] = 0.65
    
    # Information: learning purpose or information-seeking verbs
    info_action_count = action_hits.get("information", {}).get("count", 0)
    has_learning_purpose = purpose_hits.get("learning", {}).get("count", 0) > 0
    
    if info_action_count > 0 or has_learning_purpose:
        scores["information"] = min(0.5 + (info_action_count * 0.1), 1.0)
    
    # Default to information if no other intent detected (but keep score low)
    max_risk_score = max([scores.get(cat, 0.0) for cat in ["illegal", "violence", "self-harm", "manipulation", "sensitive-data", "toxicity"]], default=0.0)
    if max_risk_score == 0.0:
        # Set information score for benign queries
        if scores.get("information", 0.0) == 0.0:
            scores["information"] = 0.4  # Default for benign queries
    
    return scores


def fuse_risk(scores: Dict[str, float]) -> Tuple[List[str], float, str]:
    """
    Fuse intent scores into risk_flags, risk_score, and risk_level.
    
    Returns:
        (risk_flags, risk_score, risk_level)
    """
    risk_flags: List[str] = []
    
    # Collect risk flags based on thresholds
    if scores.get("self-harm", 0.0) >= THRESHOLD_SELF_HARM:
        risk_flags.append("self-harm")
    if scores.get("violence", 0.0) >= THRESHOLD_VIOLENCE:
        risk_flags.append("violence")
    if scores.get("illegal", 0.0) >= THRESHOLD_ILLEGAL:
        risk_flags.append("illegal")
    if scores.get("manipulation", 0.0) >= THRESHOLD_MANIPULATION:
        risk_flags.append("manipulation")
    if scores.get("sensitive-data", 0.0) >= THRESHOLD_SENSITIVE_DATA:
        risk_flags.append("sensitive-data")
    if scores.get("toxicity", 0.0) >= THRESHOLD_TOXICITY:
        risk_flags.append("toxicity")
    
    # Risk score = max of risk categories
    risk_categories = ["self-harm", "violence", "illegal", "manipulation", "sensitive-data", "toxicity"]
    risk_score = max([scores.get(cat, 0.0) for cat in risk_categories], default=0.0)
    
    # Risk level
    if risk_score >= 1.0:
        risk_level = "critical"
    elif risk_score >= 0.7:
        risk_level = "high"
    elif risk_score >= 0.4:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    return (risk_flags, risk_score, risk_level)

