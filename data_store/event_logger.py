"""
Supabase Event Logger
EZA-Core v4.0 – global logging system
"""

from datetime import datetime
from typing import Dict, Any
from backend.infra.supabase_client import insert_event


EVENT_TABLE = "eza_events"   # Supabase içinde tablo adı


def log_event(event_type: str, payload: Dict[str, Any]):
    timestamp = datetime.utcnow().isoformat()

    data = {
        "event_type": event_type,
        "timestamp": timestamp,
        "payload": payload
    }

    # Supabase'e yaz
    insert_event(EVENT_TABLE, data)

    return {
        "status": "ok",
        "timestamp": timestamp,
        "stored_in": "supabase"
    }
