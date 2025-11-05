# utils.py
import datetime
import uuid
import hashlib
import os
from typing import Optional

def now_iso():
    return datetime.datetime.utcnow().isoformat(sep=' ', timespec='seconds')

def gen_case_id() -> str:
    t = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    suffix = uuid.uuid4().hex[:6].upper()
    return f"SC-{t}-{suffix}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg="Press Enter to continue..."):
    input(msg)

def hash_password(password: str, salt: Optional[str] = None) -> str:
    if salt is None:
        salt = uuid.uuid4().hex
    h = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}${h}"

def verify_password(stored: str, provided: str) -> bool:
    try:
        salt, _ = stored.split('$', 1)
        return hash_password(provided, salt) == stored
    except Exception:
        return False
