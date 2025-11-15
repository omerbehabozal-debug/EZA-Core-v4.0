"""
Database Config – Supabase / PostgreSQL bağlantısı
"""

import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase_client() -> Client:
    """
    Supabase istemcisini oluşturur.
    - Normal işlemler için ANON KEY
    - Sunucu tarafı için SERVICE ROLE KEY
    """
    if not SUPABASE_URL:
        raise ValueError("HATA: SUPABASE_URL .env dosyasında tanımlı değil!")

    if not SUPABASE_ANON_KEY:
        raise ValueError("HATA: SUPABASE_ANON_KEY .env dosyasında tanımlı değil!")

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
