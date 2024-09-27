from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=60)

def get_cache_key(request_type: str, data: dict):
    return f"{request_type}:{hash(frozenset(data.items()))}"