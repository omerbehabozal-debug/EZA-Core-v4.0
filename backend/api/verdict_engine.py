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
        # Level-6: Use ethical_gradient and legal_risk if available
        ethical_gradient = report.get("ethical_gradient", {})
        legal_risk = report.get("legal_risk", {})
        
        # LEVEL 7 – Critical Bias Engine
        critical_bias = report.get("critical_bias") or {}
        critical_bias_level = str(critical_bias.get("level", "low"))
        critical_bias_score = float(critical_bias.get("bias_score", 0.0))
        
        # LEVEL 8 – Moral Compass Engine
        moral = report.get("moral_compass") or {}
        moral_level = str(moral.get("level", "low"))
        moral_score = float(moral.get("score", 0.0))
        
        # LEVEL 9 – Abuse & Coercion Engine
        abuse = report.get("abuse") or {}
        abuse_level = str(abuse.get("level", "low"))
        abuse_score = float(abuse.get("score", 0.0))
        
        # Initialize verdict dict
        verdict = {
            "level": "safe",
            "reason": "",
            "flags": []
        }
        
        # Check for critical legal risk
        if legal_risk and isinstance(legal_risk, dict):
            legal_level = legal_risk.get("level", "low")
            if legal_level == "critical":
                verdict["level"] = "critical"
                verdict["reason"] = "Critical legal risk detected. Interaction blocked."
                verdict["flags"].append("legal-risk-critical")
                verdict["critical_bias_level"] = critical_bias_level
                verdict["critical_bias_score"] = round(critical_bias_score, 4)
                return verdict
            elif legal_level == "high":
                verdict["level"] = "unsafe"
                verdict["reason"] = "High legal risk detected. Proceed with extreme caution."
                verdict["flags"].append("legal-risk-high")
        
        # Check ethical gradient grade if available
        if ethical_gradient and isinstance(ethical_gradient, dict):
            ethical_grade = ethical_gradient.get("grade", "")
            if ethical_grade == "F":
                verdict["level"] = "critical"
                verdict["reason"] = "Critical ethical violation detected."
                verdict["flags"].append("ethical-violation-critical")
                verdict["critical_bias_level"] = critical_bias_level
                verdict["critical_bias_score"] = round(critical_bias_score, 4)
                return verdict
            elif ethical_grade == "D":
                verdict["level"] = "unsafe"
                verdict["reason"] = "Significant ethical concerns detected."
                verdict["flags"].append("ethical-concern-high")
            elif ethical_grade == "C":
                verdict["level"] = "caution"
                verdict["reason"] = "Moderate ethical concerns. Proceed with caution."
                verdict["flags"].append("ethical-concern-moderate")
        
        # Fallback to original EZA score logic
        if eza_score["risk_grade"].startswith("A"):
            verdict["level"] = "safe"
            verdict["reason"] = "Safe interaction."
        elif eza_score["risk_grade"].startswith("B"):
            verdict["level"] = "caution"
            verdict["reason"] = "Proceed with caution."
        elif eza_score["risk_grade"].startswith("C"):
            verdict["level"] = "unsafe"
            verdict["reason"] = "High-risk behavior detected."
        else:
            verdict["level"] = "critical"
            verdict["reason"] = "Critical safety concern detected."
        
        # LEVEL 7 – Critical Bias etkisi
        bias_is_high = critical_bias_level in {"high", "critical"} or critical_bias_score >= 0.6
        
        if bias_is_high:
            # Mevcut kararı daha sıkı bir seviyeye çek
            # Örnek strateji:
            # - Eğer "Safe" ise "Caution"
            # - Eğer "Caution" ise "Unsafe"
            # - Zaten "Unsafe/Critical" ise aynı kalabilir
            level = verdict.get("level", "safe").lower()
            
            if level == "safe":
                verdict["level"] = "caution"
                verdict["reason"] = (
                    verdict.get("reason", "")
                    + " | Critical Bias Engine: yüksek önyargı riski tespit edildi."
                )
            elif level == "caution":
                verdict["level"] = "unsafe"
                verdict["reason"] = (
                    verdict.get("reason", "")
                    + " | Critical Bias Engine: yüksek önyargı riski nedeniyle seviye yükseltildi."
                )
            else:
                # unsafe / critical gibi durumlarda sadece sebebe not düş
                verdict["reason"] = (
                    verdict.get("reason", "")
                    + " | Critical Bias Engine: yüksek önyargı riski bulundu."
                )
            
            verdict.setdefault("flags", []).append("critical-bias-risk")
        
        # Add critical bias info to verdict
        verdict["critical_bias_level"] = critical_bias_level
        verdict["critical_bias_score"] = round(critical_bias_score, 4)
        
        # LEVEL 8 – Moral Compass etkisi
        moral_high = moral_level in {"high", "critical"} or moral_score >= 0.6

        if moral_high:
            lvl = verdict.get("level", "safe").lower()

            if lvl == "safe":
                verdict["level"] = "caution"
                verdict["reason"] += " | Moral Compass: yüksek etik risk tespit edildi."
            elif lvl == "caution":
                verdict["level"] = "unsafe"
                verdict["reason"] += " | Moral Compass: risk nedeniyle seviye yükseltildi."
            else:
                verdict["reason"] += " | Moral Compass: yüksek etik risk algılandı."

            verdict.setdefault("flags", []).append("moral-compass-risk")

        verdict["moral_compass_level"] = moral_level
        verdict["moral_compass_score"] = round(moral_score, 4)
        
        # LEVEL 9 – Abuse etkisi
        abuse_high = abuse_level in {"high", "critical"} or abuse_score >= 0.6

        if abuse_high:
            lvl = verdict.get("level", "safe").lower()

            # Tehdit veya şantaj durumunda güvenlik seviyesi düşürülür
            if lvl in {"safe", "caution"}:
                verdict["level"] = "unsafe"
                verdict["reason"] += " | AbuseEngine: şiddet / tehdit / baskı sinyali tespit edildi."
            else:
                verdict["reason"] += " | AbuseEngine: yüksek istismar riski bulundu."

            verdict.setdefault("flags", []).append("abuse-risk")

        verdict["abuse_level"] = abuse_level
        verdict["abuse_score"] = round(abuse_score, 4)
        
        return verdict

