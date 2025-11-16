# -*- coding: utf-8 -*-
"""
Database Config – Supabase / PostgreSQL bağlantısı
"""

import os
from pathlib import Path
from supabase import create_client, Client

# .env dosyasını yükle
try:
    from dotenv import load_dotenv
    # Proje kök dizininden .env dosyasını yükle
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv yüklü değilse devam et
    pass

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase_client() -> Client:
    """
    Supabase istemcisini oluşturur.
    - Normal işlemler için ANON KEY
    - Sunucu tarafı için SERVICE ROLE KEY
    
    Eğer .env dosyasında değerler yoksa None döndürür (opsiyonel kullanım).
    """
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError(
            "HATA: SUPABASE_URL ve SUPABASE_ANON_KEY .env dosyasında tanımlı değil!\n"
            "Lütfen proje kök dizininde .env dosyası oluşturun ve şu değişkenleri ekleyin:\n"
            "SUPABASE_URL=your_supabase_url\n"
            "SUPABASE_ANON_KEY=your_anon_key\n"
            "SUPABASE_SERVICE_ROLE_KEY=your_service_role_key (opsiyonel)"
        )

    # İstemciyi oluştur
    supabase_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return supabase_client


def get_service_client() -> Client:
    """
    Tam yetkili servis işlemleri için SERVICE ROLE KEY ile bağlanır.
    (Kullanıcı görmemeli — sadece backend tarafı)
    """
    if not SUPABASE_URL:
        raise ValueError("HATA: SUPABASE_URL .env dosyasında tanımlı değil!")

    if not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("HATA: SUPABASE_SERVICE_ROLE_KEY .env içinde tanımlı değil!")

    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
