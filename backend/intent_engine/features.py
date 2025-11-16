# -*- coding: utf-8 -*-
"""
intent_engine/features.py – EZA-IntentEngine v4.0

Multi-layer semantic feature extraction for professional intent analysis.
"""

from typing import Dict, List
import re


def extract_semantic_features(text: str) -> Dict[str, List[str]]:
    """
    Multi-layer semantic extraction:
    - Action tokens
    - Target tokens
    - Purpose tokens
    - Hidden intent signals
    - Harmful context patterns
    - Modal verbs (istek, emir, plan)
    
    Returns:
        Dictionary with modal_hits, stealth_hits, harm_hits, target_hits
    """
    t = text.lower()
    
    # Modal verbs: increases intent strength
    modal_signals = [
        "istiyorum", "nasıl", "yapabilir", "yapayım", "planlıyorum", 
        "ne yapmalıyım", "yapmak istiyorum", "yapabilir miyim",
        "yapmalıyım", "yapmam gerek", "yapmam lazım"
    ]
    modal_hits = [w for w in modal_signals if w in t]
    
    # Hidden/stealth intent
    stealth_signals = [
        "gizlice", "belli etmeden", "haberi olmadan", "çaktırmadan",
        "fark ettirmeden", "gizli", "sessizce", "habersizce"
    ]
    stealth_hits = [w for w in stealth_signals if w in t]
    
    # Purpose/harm indicators
    harm_signals = [
        "zarar", "acı", "öldür", "döv", "kötü", "mahvet", "yok et",
        "incit", "kır", "boz", "tahrip", "zedele"
    ]
    harm_hits = [w for w in harm_signals if w in t]
    
    # Target extraction
    target_signals = [
        "beni", "kendimi", "kendime", "kendim",
        "birini", "onu", "öğretmenim", "arkadaşım", "arkadasim",
        "patronum", "sevgilim", "eşim", "esim",
        "komşum", "hocam", "müdürüm", "doktorum",
        "kardeşim", "kardesim", "çocuğum", "cocugum"
    ]
    target_hits = [w for w in target_signals if w in t]
    
    return {
        "modal_hits": modal_hits,
        "stealth_hits": stealth_hits,
        "harm_hits": harm_hits,
        "target_hits": target_hits,
    }

