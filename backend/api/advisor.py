# -*- coding: utf-8 -*-
"""
advisor.py – EZA-Core v5
Risk ve alignment bilgisine göre etik tavsiye üreten katman.
"""

from typing import Any, Dict, List

from data_store.event_logger import log_event


def _has_flag(flags: List[str], flag: str) -> bool:
    return flag in flags


def generate_advice(
    input_analysis: Dict[str, Any],
    output_analysis: Dict[str, Any],
    alignment_result: Dict[str, Any],
) -> str:
    """
    Risk ve alignment bilgisine göre kullanıcıya gösterilecek etik tavsiyeyi üretir.
    Özellikle self-harm, illegal ve saldırgan içerikler için insan odaklı, güvenli
    yönlendirmeler verir.
    """
    in_flags: List[str] = input_analysis.get("risk_flags", []) or []
    out_flags: List[str] = output_analysis.get("risk_flags", []) or []
    all_flags = list(set(in_flags + out_flags))

    verdict = alignment_result.get("verdict", "Unknown")

    # Self-harm (intihar, kendine zarar)
    if _has_flag(all_flags, "self-harm"):
        advice = (
            "Bu mesaj, kendine zarar verme veya intihar riski içeriyor olabilir. "
            "Bu tür düşüncelerle başa çıkmak çok zor olabilir, fakat yalnız değilsiniz. "
            "Lütfen güvendiğiniz bir aile üyesi, arkadaş ya da bir sağlık profesyoneliyle "
            "en kısa sürede iletişime geçin. Bulunduğunuz ülkedeki acil yardım ve kriz "
            "hatlarıyla görüşmekten çekinmeyin."
        )
    # Illegal
    elif _has_flag(all_flags, "illegal"):
        advice = (
            "İçerikte yasa dışı faaliyetlere yönelik ifadeler tespit edildi. "
            "EZA, suç teşkil eden eylemlerle ilgili talimat vermez. "
            "Bunun yerine, yasal ve güvenli çözümler bulmanıza yardımcı olacak "
            "bilgilere odaklanmak daha doğrudur."
        )
    # Violence
    elif _has_flag(all_flags, "violence"):
        advice = (
            "İçerikte şiddet veya saldırgan davranışlara dair ifadeler tespit edildi. "
            "Şiddet, kalıcı fiziksel ve psikolojik zararlar doğurabilir. "
            "Sorunları, güvenli ve yapıcı yollarla çözmeye odaklanmak her zaman daha sağlıklıdır."
        )
    # Manipulation
    elif _has_flag(all_flags, "manipulation"):
        advice = (
            "İçerikte başkalarını manipüle etmeye yönelik niyetler görülebilir. "
            "Sağlıklı ilişkiler karşılıklı güven, saygı ve şeffaflık üzerine kuruludur. "
            "Manipülatif yaklaşımlar uzun vadede güveni zedeler."
        )
    # Toxicity / Hate
    elif _has_flag(all_flags, "toxicity"):
        advice = (
            "İçerikte hakaret veya toksik dil tespit edildi. "
            "Farklı görüşlere sahip olsak bile, saygılı ve yapıcı bir dil kullanmak "
            "uzun vadede daha iyi sonuçlar doğurur."
        )
    else:
        # Düşük riskli senaryolar için genel etik tavsiye
        advice = (
            "Bu içerik için ciddi bir risk tespit edilmedi. Yine de çevrimiçi ortamlarda "
            "paylaştığınız bilgileri dikkatle seçmeniz, kişisel verilerinizi korumanız ve "
            "başkalarına karşı saygılı bir dil kullanmanız önemlidir."
        )

    log_event("advice_generated", {"verdict": verdict, "flags": all_flags, "advice": advice})
    return advice
