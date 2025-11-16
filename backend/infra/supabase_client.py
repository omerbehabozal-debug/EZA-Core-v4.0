# -*- coding: utf-8 -*-
"""
Supabase CRUD helper fonksiyonları
"""

from typing import Dict, Any, Optional
from backend.infra.db_config import get_supabase_client


def insert_event(table: str, data: Dict[str, Any]) -> Optional[Any]:
    """
    Seçilen tabloya kayıt ekler.
    Supabase yapılandırılmamışsa sessizce None döndürür.
    """
    try:
        client = get_supabase_client()
        return client.table(table).insert(data).execute()
    except ValueError:
        # Supabase yapılandırılmamışsa sessizce devam et
        return None
    except Exception:
        # Diğer hatalarda da sessizce devam et (loglama yapılabilir)
        return None


def fetch_events(table: str, limit: int = 20) -> Optional[Any]:
    """
    Belirtilen tablodan son kayıtları çeker.
    Supabase yapılandırılmamışsa sessizce None döndürür.
    """
    try:
        client = get_supabase_client()
        return client.table(table).select("*").limit(limit).order("id", desc=True).execute()
    except (ValueError, Exception):
        return None


def delete_event(table: str, event_id: int) -> Optional[Any]:
    """
    Tablo üzerindeki belirli bir kaydı siler.
    Supabase yapılandırılmamışsa sessizce None döndürür.
    """
    try:
        client = get_supabase_client()
        return client.table(table).delete().eq("id", event_id).execute()
    except (ValueError, Exception):
        return None
