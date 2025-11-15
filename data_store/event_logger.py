from datetime import datetime
from backend.infra.supabase_client import insert_event


def log_event(event_type: str, payload: dict):
    """
    Supabase event_logs tablosuna kayıt ekler.
    """

    data = {
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }

    return insert_event("event_logs", data)
