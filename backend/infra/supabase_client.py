"""
Supabase CRUD helper fonksiyonları
"""

from typing import Dict, Any
from backend.infra.db_config import get_supabase_client


def insert_event(table: str, data: Dict[str, Any]):
    """
    Seçilen tabloya kayıt ekler.
    """
    client = get_supabase_client()
    return client.table(table).insert(data).execute()


def fetch_events(table: str, limit: int = 20):
    """
    Belirtilen tablodan son kayıtları çeker.
    """
    client = get_supabase_client()
    return client.table(table).select("*").limit(limit).order("id", desc=True).execute()


def delete_event(table: str, event_id: int):
    """
    Tablo üzerindeki belirli bir kaydı siler.
    """
    client = get_supabase_client()
    return client.table(table).delete().eq("id", event_id).execute()
