"""
Supabase CRUD helper fonksiyonları
"""

from typing import Dict, Any
from .db_config import get_supabase

supabase = get_supabase()

def insert_event(table: str, data: Dict[str, Any]):
    return supabase.table(table).insert(data).execute()

def fetch_events(table: str, limit: int = 20):
    return supabase.table(table).select("*").limit(limit).order("id", desc=True).execute()

def delete_event(table: str, event_id: int):
    return supabase.table(table).delete().eq("id", event_id).execute()
