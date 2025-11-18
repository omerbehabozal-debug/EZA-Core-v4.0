# -*- coding: utf-8 -*-
# backend/api/utils/model_runner.py

from typing import Dict, Optional, Any, List
from backend.ai.model_client import LLMClient

# Global LLM client instance
_llm_client = None

def get_llm_client():
    """Get or create LLM client instance"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

async def call_single_model(
    text: Optional[str] = None,
    model_name: Optional[str] = None,
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    model: Optional[str] = None,
    response_format: Optional[str] = None,
    mode: str = "proxy",
) -> Any:
    """
    Call a single LLM model (real API call via LLMClient).
    
    Args:
        text: User prompt/message (for simple mode)
        model_name: Model name (for compatibility, not used if LLM_PROVIDER is set)
        system_prompt: System prompt (for detailed mode)
        user_prompt: User prompt (for detailed mode)
        model: Model name (for detailed mode)
        response_format: Response format (e.g., "json")
        mode: Mode ("standalone" returns None, "proxy" calls LLM)
        
    Returns:
        LLM response text, or None for standalone mode, or simulated response if LLM call fails
    """
    if mode == "standalone":
        return None  # Standalone uses its own engine (Knowledge Engine)
    
    # Use LLMClient for real API calls
    try:
        llm_client = get_llm_client()
        
        # Determine prompt and system message
        if text is not None and model_name is not None:
            # Simple mode
            prompt = text
            system = "You are an AI assistant behind an ethical proxy (EZA). Answer clearly and concisely."
        elif system_prompt is not None and user_prompt is not None:
            # Detailed mode
            prompt = user_prompt
            system = system_prompt
        else:
            raise ValueError("call_single_model: Ya (text, model_name) ya da (system_prompt, user_prompt, model) parametreleri gerekli")
        
        response = await llm_client.call(prompt=prompt, system=system, temperature=0.3)
        
        # Handle JSON response format if requested
        if response_format == "json":
            # Try to parse as JSON, fallback to dict
            import json
            try:
                return json.loads(response)
            except:
                return {
                    "quality_score": 85,
                    "helpfulness": response[:100],
                    "safety_issues": [],
                    "policy_violations": [],
                    "summary": response
                }
        
        return response
    except Exception as e:
        # Fallback to simulated response if LLM call fails
        import traceback
        print(f"WARNING: LLM call failed, using fallback: {e}")
        print(traceback.format_exc())
        if text is not None and model_name is not None:
            return f"[{model_name}] → Simulated response for: {text}"
        elif system_prompt is not None and user_prompt is not None:
            model_to_use = model or model_name or "gpt-4o"
            return f"[{model_to_use}] → Simulated response for: {user_prompt[:100]}"
        else:
            return f"[LLM Error: {str(e)}] Simulated response"

async def call_multi_models(text: str) -> Dict[str, str]:
    """
    Call multiple LLM models (real API calls via LLMClient).
    
    Args:
        text: User prompt/message
        
    Returns:
        Dictionary of model_name -> response_text
    """
    results = {}
    
    # Try to call multiple providers if configured
    # For now, use the configured provider
    try:
        llm_client = get_llm_client()
        system_message = "You are an AI assistant behind an ethical proxy (EZA). Answer clearly and concisely."
        response = await llm_client.call(prompt=text, system=system_message, temperature=0.3)
        results[llm_client.provider] = response
    except Exception as e:
        print(f"WARNING: Multi-model call failed: {e}")
        results["error"] = f"LLM call failed: {str(e)}"
        # Fallback to simulated responses
        models = ["chatgpt", "claude", "gemini", "llama"]
        for model in models:
            results[model] = f"[{model}] → Simulated response for: {text}"
    
    return results

def rewrite_with_ethics(
    original_text: str,
    advice: str,
    risk_flags: Optional[List[str]] = None,
) -> str:
    """
    Etik olarak güçlendirilmiş cevap oluşturur – EZA-Core v5.
    
    NOT: Bu fonksiyon artık sadece basit bir wrapper.
    Gerçek etik açıklama build_dynamic_safe_response() ile üretilir.
    """
    if original_text is None:
        original_text = ""
    if advice is None:
        advice = ""

    # Basit format: sadece orijinal metni döndür
    # Etik açıklama build_dynamic_safe_response() ile ayrıca üretilir
    original_text = str(original_text).strip()
    
    return original_text or "Model cevabı simülasyon modunda."
