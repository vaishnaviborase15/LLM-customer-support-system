cache_store = {}

def get_cache(query):
    return cache_store.get(query.lower())

def set_cache(query, result):
    cache_store[query.lower()] = result