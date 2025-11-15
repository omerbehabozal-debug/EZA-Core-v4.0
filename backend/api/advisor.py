"""
advisor.py
----------
Alignment sonucuna göre aksiyon / tavsiye üreten katman.
"""

from typing import Any, Dict

from backend.api.utils import call_single_model
from data_store.event_logger import log_event


def _system_prompt_advisor() -> str:
    return (
        "Sen EZA-Core'un 'Ethical Advisor' katmanısın.\n"
        "Input analizi, output analizi ve alignment sonucunu alırsın;\n"
        "amacın yasaklamak değil, rehberlik etmektir.\n\n"
        "JSON formatında cevap ver:\n"
        "{\n"
        '  "user_message": "kullanıcıya sade tavsiye",\n'
        '  "developer_notes": "geliştiriciye teknik/etik notlar",\n'
        '  "risk_level": "low / medium / high",\n'
        '  "suggested_actions": ["log", "manual_review", ...]\n'
        "}"
    )


def generate_advice(
    input_analysis: Dict[str, Any],
    output_analysis: Dict[str, Any],
    alignment_result: Dict[str, Any],
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Alignment sonucuna göre kullanıcı + geliştirici için tavsiye üretir.
    """
    payload: Dict[str, Any] = {
        "stage": "advisor",
        "alignment_ok": alignment_result.get("ok"),
        "alignment_score": alignment_result.get("alignment_score"),
        "alignment_verdict": alignment_result.get("verdict"),
    }

    try:
        system_prompt = _system_prompt_advisor()

        user_prompt = (
            "Aşağıda EZA-Core katmanlarından gelen üç farklı özet var.\n\n"
            "1) Input Analysis:\n"
            f"{input_analysis}\n\n"
            "2) Output Analysis:\n"
            f"{output_analysis}\n\n"
            "3) Alignment Result:\n"
            f"{alignment_result}\n\n"
            "Görevin; kullanıcıya sade bir mesaj, geliştiriciye ise teknik/etik notlar önermektir.\n"
            "Her zaman belirtilen JSON formatında cevap ver."
        )

        llm_response = call_single_model(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            response_format="json",
        )

        result: Dict[str, Any] = {
            "ok": True,
            "model": model,
            "advice": llm_response,
            "error": None,
        }

        payload.update(
            {
                "result_ok": True,
                "risk_level": llm_response.get("risk_level"),
            }
        )
        log_event("advice_generated", payload)

        return result

    except Exception as exc:  # noqa: BLE001
        error_msg = str(exc)

        fail_result: Dict[str, Any] = {
            "ok": False,
            "model": model,
            "advice": {},
            "error": error_msg,
        }

        payload["result_ok"] = False
        payload["error"] = error_msg
        log_event("advisor_error", payload)

        return fail_result
