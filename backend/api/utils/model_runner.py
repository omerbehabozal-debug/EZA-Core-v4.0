# -*- coding: utf-8 -*-
# backend/api/utils/model_runner.py

from typing import Dict, Optional, Any, List

def call_single_model(
    text: Optional[str] = None,
    model_name: Optional[str] = None,
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    model: Optional[str] = None,
    response_format: Optional[str] = None,
) -> Any:
    """
    Tek bir modelden yanıt alır — Şu anda demo amaçlı.
    Gerçekte OpenAI / Claude / Gemini API entegre edilecek.
    
    İki kullanım modu desteklenir:
    1. Basit: call_single_model(text="...", model_name="...")
    2. Detaylı: call_single_model(system_prompt="...", user_prompt="...", model="...", response_format="...")
    """
    # Basit kullanım modu
    if text is not None and model_name is not None:
        return f"[{model_name}] → Simulated response for: {text}"
    
    # Detaylı kullanım modu
    if system_prompt is not None and user_prompt is not None:
        model_to_use = model or model_name or "gpt-4o"
        # Simüle edilmiş JSON yanıtı
        if response_format == "json":
            return {
                "quality_score": 85,
                "helpfulness": "İyi bir cevap",
                "safety_issues": [],
                "policy_violations": [],
                "summary": "Simüle edilmiş analiz sonucu"
            }
        return f"[{model_to_use}] → Simulated response for: {user_prompt[:100]}"
    
    raise ValueError("call_single_model: Ya (text, model_name) ya da (system_prompt, user_prompt, model) parametreleri gerekli")

def call_multi_models(text: str) -> Dict[str, str]:
    """
    Premium çoklu model çağırma simülasyonu.
    """
    models = ["chatgpt", "claude", "gemini", "llama"]
    
    return {
        model: f"[{model}] → Simulated response for: {text}"
        for model in models
    }

def rewrite_with_ethics(
    original_text: str,
    advice: str,
    risk_flags: Optional[List[str]] = None,
) -> str:
    """
    Etik olarak güçlendirilmiş cevap oluşturur – EZA-Core v5.

    risk_flags:
        - self-harm → krize duyarlı, destek odaklı mesaj
        - illegal / violence / manipulation → yönlendirici, zararı azaltıcı mesaj
        - aksi halde: orijinal cevabı etik çerçeveyle güçlendir.
    """
    if original_text is None:
        original_text = ""
    if advice is None:
        advice = ""

    risk_flags = risk_flags or []

    # Self-harm özel senaryosu
    if "self-harm" in risk_flags:
        return (
            "Bu mesaj, kendine zarar verme veya intihar düşüncelerini içerebilir. "
            "Böyle hissetmek çok zor olabilir, fakat yalnız değilsiniz. "
            "Buradan genel bilgiler verebilirim; ancak profesyonel destek almak çok daha önemlidir. "
            "Lütfen güvendiğiniz biriyle konuşun ve bulunduğunuz ülkedeki acil yardım hatlarıyla "
            "veya bir ruh sağlığı uzmanıyla en kısa sürede iletişime geçin."
        )

    # Yasa dışı, şiddet veya manipülasyon içeren riskli içerikler için
    if any(flag in risk_flags for flag in ["illegal", "violence", "manipulation"]):
        return (
            "Bu isteğe doğrudan yardım edemem çünkü şiddet, yasa dışı faaliyetler veya "
            "başkalarına zarar verebilecek davranışlar etik değildir. "
            "Bunun yerine, sorunları yasal, güvenli ve saygılı yollarla çözmeye odaklanmak en doğrusudur. "
            "Aşağıda, daha güvenli bir yaklaşım için genel bir yönlendirme bulabilirsiniz:\n\n"
            f"Etik Tavsiye:\n{advice}"
        )

    # Diğer tüm durumlar için – orijinal cevabı etik çerçeveyle güçlendir
    original_text = str(original_text).strip()
    advice = str(advice).strip()

    return (
        "Orijinal Cevap:\n"
        f"{original_text or 'Model cevabı simülasyon modunda.'}\n\n"
        "Etik Perspektif:\n"
        f"{advice or 'Bu içerik için özel bir risk tespit edilmedi.'}\n\n"
        "Etik Olarak Güçlendirilmiş Cevap:\n"
        f"{original_text or 'Model cevabı'}\n"
        "— Bu cevap, kullanıcı güvenliği ve saygılı iletişim ilkeleri gözetilerek değerlendirilmiştir."
    )
