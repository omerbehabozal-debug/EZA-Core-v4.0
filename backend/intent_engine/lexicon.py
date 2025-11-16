# -*- coding: utf-8 -*-
"""
intent_engine/lexicon.py – EZA-IntentEngine v3.0

Lexicon definitions for action verbs, target words, purpose clues, and risk keywords.
"""

from typing import Dict, List

# Action verbs by category
ACTION_VERBS: Dict[str, List[str]] = {
    "violence": [
        "döv", "dövmek", "döverim", "döver",
        "vur", "vurmak", "vururum",
        "bıçakla", "bıçaklamak",
        "yarala", "yaralamak",
        "öldür", "öldürmek", "öldürürüm",
        "saldır", "saldırmak", "saldırırım",
        "tekmele", "tekmelemek",
        "boğ", "boğmak",
    ],
    "illegal": [
        "çal", "çalmak", "çalış",
        "hack", "hackle", "hacklemek",
        "kır", "kırmak", "kırarım", "kırarim", "kirar",
        "kopyala", "kopyalamak",
        "dolandır", "dolandırmak",
    ],
    "self_harm": [
        "kendimi öldürmek",
        "intihar etmek",
        "kendime zarar vermek",
        "hayatıma son vermek",
        "yaşamak istemiyorum",
        "ölmek istiyorum",
    ],
    "manipulation": [
        "kandır", "kandırmak", "kandir", "kandirmak", "kandırırım",
        "yönlendir", "yönlendirmek",
        "ikna etmek",
        "manipüle", "manipule", "manipüle etmek",
        "kontrol etmek",
        "etkilemek",
        "gizlice etkilemek",
    ],
    "information": [
        "öğrenmek",
        "bilmek",
        "anlamak",
        "sormak",
        "nasıl",
    ],
}

# Target words by category
TARGET_WORDS: Dict[str, List[str]] = {
    "self": [
        "kendimi",
        "kendime",
        "kendim",
    ],
    "other_person": [
        "birini",
        "birine",
        "onu",
        "arkadaşımı",
        "arkadasimi",
        "insanlari",
        "kişiyi",
        "adamı",
        "karşımdakini",
    ],
    "system": [
        "wifi",
        "wi-fi",
        "modem",
        "banka",
        "sistem",
        "hesap",
    ],
    "identity": [
        "tc kimlik",
        "t.c. kimlik",
        "kimlik numarası",
        "şifre",
        "sifre",
        "parola",
        "iban",
    ],
}

# Purpose clues
PURPOSE_CLUES: Dict[str, List[str]] = {
    "harm": [
        "zarar vermek",
        "acı çektirmek",
    ],
    "hidden": [
        "belli etmeden",
        "haberi olmadan",
        "gizlice",
        "fark ettirmeden",
    ],
    "learning": [
        "öğrenmek istiyorum",
        "bilmek istiyorum",
        "merak ediyorum",
    ],
}

# Risk keywords (flat lists for quick matching)
SELF_HARM_KEYWORDS: List[str] = [
    "intihar",
    "intihar etmek",
    "kendimi öldürmek",
    "kendime zarar vermek",
    "hayatıma son vermek",
    "yaşamak istemiyorum",
    "yaşamak istemem",
    "ölmek istiyorum",
    "kendimi yok etmek",
    "yaşamayı bırakmak",
    "keşke ölsem",
    "artık yaşamak istemiyorum",
    "ölsem kurtulsam",
    "yaşamak anlamsız",
    "bu acıya dayanamıyorum",
    "hayat dayanılmaz",
    "kendime bir şey yapmayı düşünüyorum",
]

VIOLENCE_KEYWORDS: List[str] = [
    "öldürmek",
    "öldürürüm",
    "öldürmek istiyorum",
    "saldırmak",
    "birine saldırmak",
    "saldırırım",
    "döv",
    "döverim",
    "dövmek",
    "dövme",
    "döver",
    "dövrm",
    "dov",
    "dovmek",
    "adam dövmek",
    "kavga etmek",
    "yumruk atmak",
    "yumruklamak",
    "bıçaklamak",
    "vurmak",
    "şiddet uygulamak",
    "yaralamak",
    "boğmak",
    "kafasına vurmak",
    "itmek",
    "tekmelemek",
    "birine zarar vermek",
    "birini nasıl döverim",
    "susturmak",
    "intikam almak",
    "birini tehdit etmek",
    "nasıl saldırırım",
    "birine zarar vermek istiyorum",
    "birini öldürmek istiyorum",
]

ILLEGAL_KEYWORDS: List[str] = [
    "hack",
    "hacker",
    "hacklemek",
    "sistem hack",
    "hesap hack",
    "banka hesabı hack",
    "instagram hack",
    "facebook hack",
    "wifi şifresi kırmak",
    "wifi şifresini kırmak",
    "wifi kırmak",
    "wifi hack",
    "modem hack",
    "şifre kırmak",
    "password crack",
    "parola kırmak",
    "brute force",
    "brute-force",
    "hash kırmak",
    "keylogger",
    "trojan",
    "malware",
    "ransomware",
    "oltalama",
    "phishing",
    "sql injection",
    "ddos",
    "exploit",
    "kimlik çalmak",
    "tc çalmak",
    "veri çalmak",
    "data sızdırmak",
    "database çalmak",
    "hesap çalmak",
    "kart kopyalama",
    "kredi kartı dolandırıcılığı",
    "pos kopyalama",
    "iban çalma",
    "iban hack",
    "kara para",
    "kara para aklamak",
    "sahte para",
    "hesap ele geçirmek",
    "bomba yapmak",
    "patlayıcı üretmek",
    "silah yapmak",
    "yasa dışı silah",
    "yasa dışı silahlar",
    "uyuşturucu satmak",
    "uyuşturucu yapmak",
    "uyuşturucu üretimi",
    "yasadışı madde",
    "sahte kimlik",
    "suç işlemek",
    "suça yardım etmek",
    "yasa dışı iş",
]

MANIPULATION_KEYWORDS: List[str] = [
    "manipüle etmek",
    "kandırmak",
    "kandır",
    "kandırırım",
    "kandir",
    "kandirmak",
    "manipüle",
    "manipule",
    "hile yapmak",
    "psikolojik baskı",
    "gaslighting",
    "zihin kontrolü",
    "duygu sömürüsü",
    "yönlendirmek",
    "etkilemek",
    "ikna etmek",
    "baskı kurmak",
    "gizlice etkilemek",
    "zihinsel oyun",
    "aldatmak",
]

SENSITIVE_DATA_KEYWORDS: List[str] = [
    "tc kimlik",
    "t.c. kimlik",
    "kimlik numarası",
    "şifre",
    "sifre",
    "parola",
    "iban",
    "adres",
    "telefon numarası",
    "kredi kartı",
    "kişisel veri",
    "kişisel bilgi",
    "kişisel bilgiler",
]

TOXICITY_KEYWORDS: List[str] = [
    "aptal",
    "salak",
    "gerizekalı",
    "geri zekalı",
    "embesil",
    "mal",
    "öküz",
    "şerefsiz",
    "hakaret",
    "pislik",
    "nefret ediyorum",
    "nefret",
    "ırkçı",
    "ırkçılık",
    "aşağılama",
]

# Sensitive Data Signals - Level-3 Mega Patch v1.0
SENSITIVE_DATA_SIGNALS: Dict[str, List[str]] = {
    "id_numbers": [
        "tc kimlik", "tc no", "kimlik numarası", "passport", "pasaport",
        "id number", "identity number", "social security", "ssn", 
        "nüfus cüzdanı", "ehliyet no", "iban", "hesap numarası",
        "credit card", "kart numarası", "security code", "cvv"
    ],
    "personal_identifiers": [
        "annemin adı", "babamın adı", "doğum tarihi", "adresim",
        "okul numarası", "öğrenci numarası", "kimlik bilgisi",
        "telefon numarası", "mail adresi"
    ],
    "relational_targets": [
        "öğretmenim", "hocam", "patronum", "komşum", "arkadaşım",
        "sevgilim", "eşim", "kardeşim", "çocuğum", "doktorum",
        "müdürüm", "çalışanım", "danışanım"
    ],
    "lookup_patterns": [
        "nasıl bulurum", "nasıl öğrenirim", "nereden bulurum",
        "gizlice", "haberi olmadan", "izinsiz", "bana söyler misin",
        "paylaşır mısın", "elde ederim", "çıkartabilir misin",
        "belli etmeden", "habersizce"
    ]
}

