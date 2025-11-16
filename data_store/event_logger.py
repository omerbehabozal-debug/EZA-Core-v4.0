# -*- coding: utf-8 -*-
from datetime import datetime
from backend.infra.supabase_client import insert_event


def log_event(event_type: str, payload: dict):
    """
    Supabase event_logs tablosuna kayıt ekler.
    Supabase yapılandırılmamışsa sessizce devam eder.
    """

    data = {
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }

    try:
        return insert_event("event_logs", data)
    except Exception:
        # Supabase yapılandırılmamışsa veya hata oluşursa sessizce devam et
        pass
    return None
