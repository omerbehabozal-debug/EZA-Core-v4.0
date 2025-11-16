# -*- coding: utf-8 -*-
"""
loader.py – EZA-Core v6
Utility functions to load JSON-based risk dictionaries.

Core dictionaries are stored under:
backend/risk_dictionaries/core/<category>.<language>.json

Example categories:
- self_harm
- illegal
- violence
- manipulation
- sensitive_data
- toxicity
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent


def load_core_dicts(language: str = "tr") -> Dict[str, List[str]]:
    """
    Load core risk dictionaries for a given language.
    If a file is missing or invalid, returns an empty list for that category.

    core directory structure:
    backend/risk_dictionaries/core/<category>.<language>.json
    """
    core_dir = BASE_DIR / "core"
    categories = [
        "self_harm",
        "illegal",
        "violence",
        "manipulation",
        "sensitive_data",
        "toxicity",
    ]

    result: Dict[str, List[str]] = {}

    for cat in categories:
        filename = f"{cat}.{language}.json"
        path = core_dir / filename

        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    # Normalize to list of strings
                    result[cat] = [str(x).lower() for x in data]
                else:
                    result[cat] = []
            except Exception:
                result[cat] = []
        else:
            result[cat] = []

    return result


def load_domain_dicts(domain: str, language: str = "tr") -> Dict[str, List[str]]:
    """
    Placeholder for future domain-specific risk dictionaries.

    Expected structure:
    backend/risk_dictionaries/domains/<domain>/<category>.<language>.json

    For now, returns empty dict; designed for future expansion.
    """
    # This is intentionally a placeholder for Level 3 domain-specific risk.
    # You can implement finance / cybersec / health / politics later.
    _ = domain, language  # avoid unused param warnings
    return {}

