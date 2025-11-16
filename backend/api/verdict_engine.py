# -*- coding: utf-8 -*-
"""
VerdictEngine – EZA Level-5 Upgrade
Tüm analiz katmanlarını birleştirip tek cümlelik 
final etik karar üretir.
"""


class VerdictEngine:
    """
    Tüm analiz katmanlarını birleştirip tek cümlelik 
    final etik karar üretir.
    """

    def generate(self, report, eza_score, drift):
        if eza_score["risk_grade"].startswith("A"):
            return "Safe interaction."
        if eza_score["risk_grade"].startswith("B"):
            return "Proceed with caution."
        if eza_score["risk_grade"].startswith("C"):
            return "High-risk behavior detected."
        return "Critical safety concern detected."

