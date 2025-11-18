# -*- coding: utf-8 -*-
"""
advisor.py — EZA-Core v10.2

Niyet + risk + alignment çıktılarına göre:
- Etik tavsiye metni
- Etik olarak güçlendirilmiş cevap

üretilmesinden sorumlu katman.
"""

from typing import Any, Dict, Optional

from backend.api.utils.model_runner import rewrite_with_ethics

# -----------------------------------------------
# Dynamic Ethical Safety Advisor Template System
# -----------------------------------------------

SAFE_TEMPLATE = """
Bu içerikte herhangi bir risk tespit edilmedi.
Soru etik, güvenli ve bilgilendirici kategoride değerlendirilmiştir.

Kısa Analiz:

{analysis_summary}

EZA, bu tür nötr veya bilgi amaçlı sorularda yalnızca içerik analizi yapar
ve kullanıcıyı yönlendirmek için gereksiz uyarılar üretmez.
"""

LOW_RISK_TEMPLATE = """
İçerikte düşük seviyede risk unsuru tespit edildi.
Bu, kötü niyet olmadığı halde bazı ifadelerin yanlış anlaşılabilir
veya belirli hassas konulara temas ediyor olabileceği anlamına gelir.

Kısa Analiz:

{analysis_summary}

Öneri:

- Daha net ifade kullanabilirsiniz.

- Konuyu açıklığa kavuşturmak yanlış anlamaları önler.
"""

MEDIUM_RISK_TEMPLATE = """
Bu içerikte orta seviyede bir etik risk tespit edildi.
Bu, bazı ifadelerin baskı, manipülasyon, önyargı veya hassas konuları 
içerebileceği anlamına gelir.

Kısa Analiz:

{analysis_summary}

Etik Öneri:

- Dile dikkat edilmesi faydalıdır.

- Bu tür konularda daha kapsayıcı, saygılı ve dikkatli bir dil önerilir.
"""

HIGH_RISK_TEMPLATE = """
Bu içerikte yüksek etik risk tespit edildi.
Mesaj, zarar verici davranış, baskı, manipülasyon, önyargı veya hukuki
sorun oluşturabilecek ifadeler içeriyor olabilir.

Kısa Analiz:

{analysis_summary}

EZA Önerisi:

- Bu konuda profesyonel destek almak daha doğru olabilir.

- Yasal, güvenli ve saygılı yollarla hareket etmek önemlidir.
"""

CRITICAL_RISK_TEMPLATE = """
⚠ Kritik Etik Risk Tespit Edildi

Bu içerik, güvenlik açısından ciddi tehdit, hukuki sorun, zarar,
şiddet veya ağır manipülasyon potansiyeli taşıyor olabilir.

Kısa Analiz:

{analysis_summary}

EZA Tavsiyesi:

- Bu tür taleplerle ilgili doğrudan yardım sunulmaz.

- Güvenli ve yasal davranış biçimleri dışına çıkmamanız önemlidir.
"""


def build_dynamic_safe_response(report: dict) -> str:
    """
    EZA'nın final verdict seviyesine göre uygun etik yanıtı üretir.
    
    For greeting/casual/smalltalk messages, returns empty string (no advisory).
    """
    # Check if this is a greeting/casual/smalltalk message
    if _is_greeting_message(report):
        return ""  # No advisory for greeting messages

    level = (report.get("final_verdict", {}) or {}).get("level", "safe").lower()
    summary = report.get("final_verdict", {}).get("reason", "")

    if level == "safe":
        return SAFE_TEMPLATE.format(analysis_summary=summary).strip()

    if level == "low":
        return LOW_RISK_TEMPLATE.format(analysis_summary=summary).strip()

    if level == "caution":
        return MEDIUM_RISK_TEMPLATE.format(analysis_summary=summary).strip()

    if level == "unsafe":
        return HIGH_RISK_TEMPLATE.format(analysis_summary=summary).strip()

    if level == "critical":
        return CRITICAL_RISK_TEMPLATE.format(analysis_summary=summary).strip()

    # fallback
    return SAFE_TEMPLATE.format(analysis_summary=summary).strip()


def _is_greeting_message(report: Dict[str, Any]) -> bool:
    """
    Check if the message is a greeting, casual, or smalltalk message.
    ONLY pure greetings, NOT information questions with greeting words.
    """
    # Check intent from intent_engine (most reliable)
    intent_data = report.get("intent", {})
    if isinstance(intent_data, dict):
        primary = intent_data.get("primary", "").lower()
        if primary == "greeting":
            return True
    
    # Also check intent_engine directly
    intent_engine = report.get("intent_engine", {})
    if isinstance(intent_engine, dict):
        primary = intent_engine.get("primary", "").lower()
        if primary == "greeting":
            return True
    
    # Check input text for greeting patterns (fallback, but be strict)
    input_data = report.get("input", {})
    if isinstance(input_data, dict):
        raw_text = input_data.get("raw_text", "").lower()
        
        # Information question patterns - if these exist, it's NOT a greeting
        information_patterns = [
            "nedir", "ne demek", "ne anlama", "what is", "what does",
            "nasıl çalışır", "nasil calisir", "how does", "how works",
            "neden", "niçin", "why", "why does",
            "açıkla", "acikla", "explain", "tell me",
            "bilgi ver", "bilgi", "information", "info",
            "bana anlat", "bana açıkla", "bana bilgi"
        ]
        
        # If information pattern exists, it's NOT a greeting
        if any(pattern in raw_text for pattern in information_patterns):
            return False
        
        # Pure greeting keywords (only if no information pattern)
        pure_greeting_keywords = [
            "selam", "merhaba", "hey", "hi", "hello",
            "naber", "nasılsın", "nasilsin", "nasılsınız", "nasilsiniz",
            "günaydın", "gunaydin", "iyi günler", "iyi gunler"
        ]
        
        if any(keyword in raw_text for keyword in pure_greeting_keywords):
            # Additional check: must be short message
            words = raw_text.split()
            if len(words) <= 8:  # Short messages only
                return True
    
    return False


def build_standalone_response(report: Dict[str, Any], model_output: Optional[str] = None, mode: Optional[str] = None) -> str:
    """
    Standalone modda kullanıcıya gösterilecek nihai cevabı üretir.
    Yeni dinamik şablon sistemini kullanır.
    
    For greeting/casual/smalltalk messages, returns natural response without
    simulated response, EZA Advisory, or analysis text.
    """
    try:
        # Check if this is a greeting/casual/smalltalk message
        if _is_greeting_message(report):
            # Return natural greeting response only
            return "Selam! Buradayım, hazırım. Sana nasıl yardımcı olabilirim? 😊"
        
        # 1) Model cevabını al (eğer varsa)
        if model_output is None:
            # Try to get from report
            model_outputs = report.get("model_outputs", {})
            if isinstance(model_outputs, dict):
                model_output = model_outputs.get("chatgpt") or model_outputs.get(list(model_outputs.keys())[0] if model_outputs else None, "")
            else:
                model_output = str(model_outputs) if model_outputs else ""
        
        # Clean up model output (remove simulation prefix if present)
        if model_output and model_output.startswith("["):
            # Keep the model output as is, but we'll format it nicely
            pass
        
        # 2) Dinamik etik açıklama:
        advisory = build_dynamic_safe_response(report)
        
        # 3) Verdict bilgisi (not used in output, but kept for potential future use)
        verdict = report.get("final_verdict", {}) or {}
        eza_score_data = report.get("eza_score", {}) or {}
        # eza_score can be a dict with "final_score" or a number
        if isinstance(eza_score_data, dict):
            eza_score = eza_score_data.get("final_score", 0.0)
        else:
            eza_score = float(eza_score_data) if eza_score_data else 0.0

        # 4) Kullanıcıya göstereceğimiz metin:
        parts = []
        
        # Model cevabı varsa ekle
        if model_output and model_output.strip():
            parts.append(model_output.strip())
        
        # Etik açıklama - only add if not in standalone mode with Knowledge Engine
        # In standalone mode, we want natural conversation without advisory
        if mode != "standalone" or not model_output or not model_output.strip():
            # Add advisory for non-standalone modes or if no model output
            if advisory and advisory.strip():
                parts.append(f"\n\n[EZA Advisory]\n{advisory.strip()}")
        
        return "\n".join(parts)
    except Exception as e:
        # Fallback: return simple format if something goes wrong
        import traceback
        print(f"ERROR in build_standalone_response: {e}")
        print(traceback.format_exc())
        model_output = model_output or report.get("model_outputs", {}).get("chatgpt", "") if isinstance(report.get("model_outputs"), dict) else str(report.get("model_outputs", ""))
        return f"{model_output}\n\n[EZA Advisory]\nEtik analiz tamamlandı."


def _advice_for_self_harm() -> str:
    return (
        "Bu mesaj, kendine zarar verme veya intihar riski içeriyor olabilir. "
        "Bu tür düşüncelerle başa çıkmak çok zor olabilir, fakat yalnız değilsiniz. "
        "Lütfen güvendiğiniz bir aile üyesi, arkadaş ya da bir sağlık profesyoneliyle "
        "en kısa sürede iletişime geçin. Bulunduğunuz ülkedeki acil yardım ve kriz "
        "hatlarıyla görüşmekten çekinmeyin."
    )


def _advice_for_violence() -> str:
    return (
        "İçerikte şiddet veya saldırgan davranışlara dair ifadeler tespit edildi. "
        "Şiddet, kalıcı fiziksel ve psikolojik zararlar doğurabilir. "
        "Sorunları, güvenli ve yapıcı yollarla çözmeye odaklanmak her zaman daha sağlıklıdır."
    )


def _advice_for_illegal() -> str:
    return (
        "İçerikte yasa dışı faaliyetlere yönelik ifadeler tespit edildi. "
        "EZA, suç teşkil eden eylemlerle ilgili talimat vermez. "
        "Bunun yerine, yasal ve güvenli çözümler bulmanıza yardımcı olacak bilgilere "
        "odaklanmak daha doğrudur."
    )


def _advice_for_manipulation() -> str:
    return (
        "İçerikte başkalarını manipüle etmeye yönelik niyetler görülebilir. "
        "Sağlıklı ilişkiler karşılıklı güven, saygı ve şeffaflık üzerine kuruludur. "
        "Manipülatif yaklaşımlar uzun vadede güveni zedeler."
    )


def _advice_for_sensitive_data() -> str:
    return (
        "Bu içerikte kişisel veri talebi tespit edildi. "
        "EZA, kimlik bilgileri veya özel kişisel verilerle ilgili "
        "yönlendirme yapmaz. Güvenlik ve gizlilik önceliklidir. "
        "Çevrimiçi ortamlarda paylaştığınız kimlik, finansal bilgi ve şifreler gibi "
        "verileri dikkatle korumanız, üçüncü kişilerle paylaşmamanız çok önemlidir."
    )


def _advice_for_toxicity() -> str:
    return (
        "İçerikte sert, kırıcı veya toksik ifadeler bulunuyor olabilir. "
        "Farklı görüşlere sahip olsak bile, saygılı ve yapıcı bir dil kullanmak "
        "uzun vadede daha iyi sonuçlar doğurur."
    )


def _advice_for_safe() -> str:
    return (
        "Bu içerik için ciddi bir risk tespit edilmedi. "
        "Yine de çevrimiçi ortamlarda paylaştığınız bilgileri dikkatle seçmeniz, "
        "kişisel verilerinizi korumanız ve başkalarına karşı saygılı bir dil kullanmanız önemlidir."
    )


def _pick_dominant_category(
    alignment_meta: Dict[str, Any],
) -> str:
    """
    alignment_engine tarafından dönen dominant_category varsa onu al,
    yoksa risk_flags içinden öncelik sırasına göre seç.
    """
    dominant = alignment_meta.get("dominant_category")
    if dominant:
        return dominant

    risk_flags = alignment_meta.get("risk_flags") or []

    priority = [
        "self-harm",
        "violence",
        "illegal",
        "manipulation",
        "sensitive-data",
        "toxicity",
    ]
    for cat in priority:
        if cat in risk_flags:
            return cat

    return "safe"


def generate_advice(
    input_analysis: Dict[str, Any],
    output_analysis: Dict[str, Any],
    alignment_meta: Dict[str, Any],
    report: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Alignment sonucuna ve risklere göre etik tavsiye metnini üretir.
    Yeni dinamik şablon sistemi kullanılır (final_verdict varsa).
    """
    # Try to use new dynamic template system if final_verdict is available
    # Check report parameter first, then input_analysis
    if report is None:
        report = input_analysis.get("report") or input_analysis
    if isinstance(report, dict) and report.get("final_verdict"):
        try:
            return build_dynamic_safe_response(report)
        except Exception:
            pass  # Fall back to old system if new system fails
    
    # EZA-IdentityBlock v3.0: Check identity risk first (highest priority)
    identity_info = input_analysis.get("identity_block") or input_analysis.get("analysis", {}).get("identity", {})
    if identity_info and isinstance(identity_info, dict):
        identity_risk = identity_info.get("identity_risk_score", 0.0)
        if identity_risk > 0.5:
            return (
                "Bu içerik yüz tanıma, kimlik çıkarımı veya kişisel bilgi tespiti riski içerdiğinden yardımcı olamam. "
                "Kişisel verilerin korunması ve gizlilik hakları önceliklidir."
            )
    
    # EZA-NarrativeEngine v4.0: Check narrative risk
    narrative_info = input_analysis.get("analysis", {}).get("narrative", {})
    if narrative_info and isinstance(narrative_info, dict):
        narrative_score = narrative_info.get("narrative_score", 0.0)
        if narrative_score > 0.5:
            return (
                "Konuşma akışında risk artışı veya manipülatif bir gelişim tespit edildi. "
                "Bu nedenle yardımcı olamam."
            )
    
    # EZA-ReasoningShield v5.0: Check shield result
    shield = input_analysis.get("analysis", {}).get("shield", {})
    if shield and isinstance(shield, dict):
        level = shield.get("level")
        alignment_score = shield.get("alignment_score", 100)
        issues = shield.get("issues", [])
        
        if level == "critical":
            return (
                "Bu içerikte ciddi etik ve güvenlik riskleri tespit edildi. "
                "EZA, yasa dışı, şiddet içeren, kendine veya başkalarına zarar verme "
                "veya gizli manipülasyon içeren isteklere destek vermez."
            )
        elif level == "caution":
            return (
                "Bu istekte bazı riskli öğeler ve tartışmalı ifadeler bulundu. "
                "Lütfen başkalarının haklarına, mahremiyetine ve güvenliğine saygı göstererek hareket edin."
            )
    
    category = _pick_dominant_category(alignment_meta)

    if category == "self-harm":
        return _advice_for_self_harm()
    if category == "violence":
        return _advice_for_violence()
    if category == "illegal":
        return _advice_for_illegal()
    if category == "manipulation":
        return _advice_for_manipulation()
    if category == "sensitive-data":
        return _advice_for_sensitive_data()
    if category == "toxicity":
        return _advice_for_toxicity()

    return _advice_for_safe()


def generate_safe_rewrite(result: Dict[str, Any]) -> str:
    """
    EZA-IntentEngine v4.0: Generate safe rewrite based on intent and risk level.
    
    Args:
        result: Dictionary containing intent and risk_level
        
    Returns:
        Safe rewritten text
    """
    intent = result.get("intent", {})
    primary_intent = intent.get("primary", "information") if isinstance(intent, dict) else str(intent)
    risk = result.get("risk_level", "low")
    
    if risk == "critical":
        return (
            "Bu içerik yüksek riskli davranış, şiddet, kişisel veri ihlali veya "
            "başkasına zarar verme isteği içerebilir. EZA bu tür taleplere destek vermez. "
            "Daha güvenli ve yasal yollarla ilerlemek en doğrusudur."
        )
    elif risk == "high":
        return (
            "İçerikte riskli veya hassas ifadeler olabilir. "
            "EZA, güvenli ve etik şekilde yönlendirme yapmayı tercih eder."
        )
    else:
        return result.get("output_text", "")


def generate_rewritten_answer(
    original_answer: str,
    advice_text: str,
    alignment_meta: Dict[str, Any],
    report: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Etik olarak güçlendirilmiş cevabı üretir.
    Yeni dinamik şablon sistemi kullanılır (report ve final_verdict varsa).
    """
    # Try to use new dynamic template system if report is available
    if report and isinstance(report, dict) and report.get("final_verdict"):
        try:
            # Use dynamic template system for advisory
            advisory = build_dynamic_safe_response(report)
            
            # Build the final response with base output and advisory
            base = rewrite_with_ethics(original_answer, advice_text)
            
            return (
                f"{base}\n\n"
                f"[EZA Advisory]:\n"
                f"{advisory}"
            )
        except Exception:
            pass  # Fall back to old system if new system fails
    
    # Fallback: Use old system if report is not available
    # Sadece base output döndür, eski alignment metni kaldırıldı
    base = rewrite_with_ethics(original_answer, advice_text)
    return base
