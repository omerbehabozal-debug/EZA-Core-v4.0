import time
from typing import Dict
from .exceptions import RateLimitExceeded


RATE_LIMIT = 5  # 5 request
WINDOW = 10     # 10 seconds


class RateLimiter:
    def __init__(self):
        self.users: Dict[str, list] = {}

    def check(self, user_id: str):
        now = time.time()
        window_start = now - WINDOW

        if user_id not in self.users:
            self.users[user_id] = []

        # Eski kayıtları temizle
        self.users[user_id] = [
            ts for ts in self.users[user_id] if ts > window_start
        ]

        if len(self.users[user_id]) >= RATE_LIMIT:
            raise RateLimitExceeded("API kullanım limiti aşıldı.")

        self.users[user_id].append(now)


rate_limiter = RateLimiter()
