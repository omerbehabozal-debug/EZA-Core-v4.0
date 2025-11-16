# -*- coding: utf-8 -*-
"""
policy_config.py – EZA-Core v11.0

Risk eşikleri ve kategori ağırlıkları için merkezi yapılandırma.
"""

# Risk seviyesi eşikleri
RISK_THRESHOLDS = {
    "low": 0.0,
    "medium": 0.35,
    "high": 0.7,
    "critical": 0.9,
}

# Kategori baz ağırlıkları
CATEGORY_BASE_WEIGHTS = {
    "illegal": 1.0,
    "violence": 1.0,
    "self-harm": 1.0,
    "manipulation": 0.9,
    "sensitive-data": 0.85,
    "toxicity": 0.7,
    "information": 0.2,
}

# EZA Alignment skoru (0–100) için taban katsayılar
ALIGNMENT_BASE = {
    "illegal": 0,
    "violence": 5,
    "self-harm": 0,
    "manipulation": 15,
    "sensitive-data": 20,
    "toxicity": 35,
    "information": 100,
}

