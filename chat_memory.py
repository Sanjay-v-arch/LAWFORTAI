# chat_memory.py

from collections import defaultdict

# In-memory session store
SESSION_MEMORY = defaultdict(dict)

def get_session(ip: str):
    return SESSION_MEMORY[ip]

def update_session(ip: str, data: dict):
    SESSION_MEMORY[ip].update(data)

def clear_session(ip: str):
    SESSION_MEMORY[ip] = {}
