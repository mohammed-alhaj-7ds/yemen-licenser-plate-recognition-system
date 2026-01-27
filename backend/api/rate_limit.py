"""
In-memory rate limit: 60 requests per minute per IP.
Thread-safe; per-worker (suitable for single-node deployment).
"""
import threading
import time
from collections import defaultdict

_storage = defaultdict(int)
_lock = threading.Lock()
LIMIT = 60


def _minute_ts():
    return int(time.time() // 60)


def is_rate_limited(ip: str, limit: int = LIMIT) -> bool:
    key = (ip, _minute_ts())
    with _lock:
        count = _storage[key]
        if count >= limit:
            return True
        _storage[key] = count + 1
    return False


def get_remaining(ip: str, limit: int = LIMIT) -> int:
    key = (ip, _minute_ts())
    with _lock:
        count = _storage[key]
    return max(0, limit - count)
