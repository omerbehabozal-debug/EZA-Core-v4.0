# -*- coding: utf-8 -*-
# backend/api/utils/model_runner.py

from typing import Dict, Optional, Any

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

def call_multi_models(text: str, models: Optional[list] = None) -> Dict[str, str]:
    """
    Premium çoklu model çağırma simülasyonu.
    """
    if models is None:
        models = ["chatgpt", "claude", "gemini", "llama"]
    
    return {
        model: f"[{model}] → Simulated response for: {text}"
        for model in models
    }

def rewrite_with_ethics(
    text: Optional[str] = None,
    original_text: Optional[str] = None,
    advice: Optional[str] = None,
    model_name: Optional[str] = None,
) -> str:
    """
    Modele gelen etik tavsiyelerle iyileştirilmiş cevap üretir.
    """
    original = text or original_text or ""
    advice_text = advice or ""
    
    return (
        f"Orijinal: {original}\n\n"
        f"Tavsiye: {advice_text}\n\n"
        f"Etik Olarak Güçlendirilmiş Cevap:\n"
        f"{original} (etik rehberliğe göre yeniden düzenlenmiştir.)"
    )
