# -*- coding: utf-8 -*-
"""
intent_engine/dictionaries.py – EZA-IntentEngine v4.0

Dictionary exports for feature extraction and intent scoring.
"""

from .lexicon import (
    ACTION_VERBS,
    ILLEGAL_KEYWORDS,
    VIOLENCE_KEYWORDS,
    MANIPULATION_KEYWORDS,
    SENSITIVE_DATA_SIGNALS,
    TOXICITY_KEYWORDS,
)

# Flatten action verbs for easier matching
illegal_actions = ACTION_VERBS.get("illegal", []) + ILLEGAL_KEYWORDS
violence_actions = ACTION_VERBS.get("violence", []) + VIOLENCE_KEYWORDS
manipulation_actions = ACTION_VERBS.get("manipulation", []) + MANIPULATION_KEYWORDS

# Sensitive data signals (flatten from dict structure)
sensitive_data_signals = []
if SENSITIVE_DATA_SIGNALS:
    for category, items in SENSITIVE_DATA_SIGNALS.items():
        if isinstance(items, list):
            sensitive_data_signals.extend(items)

# Toxicity signals
toxicity_signals = TOXICITY_KEYWORDS

