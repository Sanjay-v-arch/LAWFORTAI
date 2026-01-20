# nlp/memory.py

_context_store = {}

def save_context(user_id: str, key: str, value: str):
    if user_id not in _context_store:
        _context_store[user_id] = {}
    _context_store[user_id][key] = value

def get_context(user_id: str, key: str):
    return _context_store.get(user_id, {}).get(key)

def get_full_context(user_id: str):
    return _context_store.get(user_id, {})
