import time
from typing import Any, Dict


class SimpleCache:
    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.expiry: Dict[str, float] = {}

    def set(self, key: str, value: Any, ttl: int = 30):
        self.store[key] = value
        self.expiry[key] = time.time() + ttl

    def get(self, key: str):
        if key not in self.store:
            return None

        if time.time() > self.expiry.get(key, 0):
            del self.store[key]
            del self.expiry[key]
            return None

        return self.store[key]


cache = SimpleCache()
