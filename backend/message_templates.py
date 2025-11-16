# -*- coding: utf-8 -*-
"""
message_templates.py – EZA-Core v11.0

EZA Tavsiyesi ve Etik Cevap şablonları.
"""

from typing import Literal

RiskLevel = Literal["low", "medium", "high", "critical"]


def get_advice_for_category(category: str, risk_level: RiskLevel) -> str:
    """
    EZA Tavsiyesi (kısa paragraf) — kategori + risk seviyesine göre TR metin.
    """
    
    # SELF-HARM
    if category == "self-harm":
        return (
            "Bu mesaj, kendine zarar verme veya intihar riski içeriyor olabilir. "
            "Böyle hissetmek çok zor olabilir, fakat yalnız değilsiniz. "
            "Lütfen güvendiğiniz biriyle ve mümkünse bir ruh sağlığı uzmanıyla "
            "en kısa sürede iletişime geçin."
        )
    
    # VIOLENCE
    if category == "violence":
        return (
            "İçerikte şiddet veya saldırgan davranışlara dair ifadeler tespit edildi. "
            "Şiddet, kalıcı fiziksel ve psikolojik zararlara yol açabilir. "
            "Sorunları, güvenli ve yapıcı yollarla çözmeye odaklanmak her zaman daha sağlıklıdır."
        )
    
    # ILLEGAL
    if category == "illegal":
        return (
            "İçerikte yasa dışı faaliyetlere yönelik ifadeler tespit edildi. "
            "EZA, suç teşkil eden eylemlerle ilgili talimat vermez. "
            "Yasal ve güvenli çözümler bulmaya odaklanmak en doğrusudur."
        )
    
    # SENSITIVE-DATA
    if category == "sensitive-data":
        return (
            "Bu içerik, başkalarına ait özel veya hassas kişisel verilerle ilgili olabilir. "
            "Kişisel verileri izinsiz paylaşmak veya elde etmeye çalışmak hem etik değildir "
            "hem de hukuki sonuçlar doğurabilir."
        )
    
    # MANIPULATION
    if category == "manipulation":
        return (
            "İçerikte başkalarını manipüle etmeye yönelik niyetler görülebilir. "
            "Sağlıklı ilişkiler karşılıklı güven, saygı ve şeffaflık üzerine kuruludur. "
            "Manipülatif yaklaşımlar uzun vadede güveni zedeler."
        )
    
    # TOXICITY
    if category == "toxicity":
        return (
            "İçerikte sert, kırıcı veya toksik ifadeler bulunuyor olabilir. "
            "Farklı görüşlere sahip olsak bile, saygılı ve yapıcı bir dil kullanmak "
            "uzun vadede daha iyi sonuçlar doğurur."
        )
    
    # INFORMATION / SAFE
    return (
        "Bu içerik için ciddi bir risk tespit edilmedi. "
        "Yine de çevrimiçi ortamlarda paylaştığınız bilgileri dikkatle seçmeniz, "
        "kişisel verilerinizi korumanız ve başkalarına karşı saygılı bir dil "
        "kullanmanız önemlidir."
    )


def get_ethically_enhanced_answer(original_output: str, category: str, risk_level: RiskLevel) -> str:
    """
    Etik Olarak Güçlendirilmiş Cevap:
    - Yüksek / kritik riskte: talebi reddet + kısa açıklama
    - Düşük riskte: orijinal cevabı koru + etik çerçeve ekle
    """
    
    # Kritik risklerde direkt yardım yok
    if risk_level == "critical":
        return (
            "Bu isteğe doğrudan yardım edemem çünkü yüksek riskli veya zararlı bir içerik barındırıyor olabilir. "
            "Sorunları yasal, güvenli ve başkalarına zarar vermeyecek yollarla çözmek en doğrusudur."
        )
    
    # Yüksek risk: uyarı + yumuşak yaklaşım
    if risk_level == "high":
        return (
            "Bu isteğe doğrudan teknik destek veremem çünkü etik ve güvenlik açısından riskler içeriyor olabilir. "
            "Buna rağmen, daha sağlıklı ve güvenli alternatif yollar düşünmek her zaman mümkündür."
        )
    
    # Orta risk: orijinali hafifçe yumuşat, etik çerçeve ekle (ileride geliştirilebilir)
    if risk_level == "medium":
        return (
            f"{original_output}\n\n"
            "— Bu cevap, daha saygılı ve yapıcı bir iletişim dili benimsemek amacıyla "
            "etik ilkeler gözetilerek değerlendirilmiştir."
        )
    
    # Düşük risk / güvenli: orijinali tut + kısa etik not
    return (
        f"{original_output}\n"
        "— Bu cevap, kullanıcı güvenliği ve saygılı iletişim ilkeleri gözetilerek değerlendirilmiştir."
    )

