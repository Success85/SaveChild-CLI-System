# data_handler.py
import sqlite3
from typing import Generator
from utils import now_iso, hash_password
DB_FILE = "safechild.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin','officer')),
        full_name TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT UNIQUE NOT NULL,
        reporter_name TEXT,
        reporter_contact TEXT,
        victim_name TEXT,
        victim_age INTEGER,
        victim_gender TEXT,
        abuse_type TEXT,
        location TEXT,
        description TEXT,
        status TEXT NOT NULL,
        assigned_officer_id INTEGER,
        created_at TEXT,
        last_updated TEXT,
        FOREIGN KEY (assigned_officer_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        user_id INTEGER,
        note TEXT,
        created_at TEXT,
        FOREIGN KEY (case_id) REFERENCES cases(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS helplines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        abuse_type TEXT NOT NULL,
        location TEXT NOT NULL,
        contact TEXT NOT NULL
    )
    """)

    conn.commit()

    # Create default admin if none exists
    cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if cur.fetchone()[0] == 0:
        admin_user = "admin"
        admin_pass = "admin123"
        cur.execute(
            "INSERT INTO users (username, password_hash, role, full_name, created_at) VALUES (?,?,?,?,?)",
            (admin_user, hash_password(admin_pass), 'admin', 'System Administrator', now_iso())
        )
        conn.commit()
        print(f"[INIT] Default admin -> {admin_user} / {admin_pass}")

    # Create a sample officer if none exists
    cur.execute("SELECT COUNT(*) FROM users WHERE role='officer'")
    if cur.fetchone()[0] == 0:
        off_user = "officer1"
        off_pass = "officer123"
        cur.execute(
            "INSERT INTO users (username, password_hash, role, full_name, created_at) VALUES (?,?,?,?,?)",
            (off_user, hash_password(off_pass), 'officer', 'Officer One', now_iso())
        )
        conn.commit()
        print(f"[INIT] Sample officer -> {off_user} / {off_pass}")

    # Default helplines if empty
    cur.execute("SELECT COUNT(*) FROM helplines")
    if cur.fetchone()[0] == 0:
        defaults = [
            ("physical", "Kigali", "Health Center A: +250 78 000 0001"),
            ("sexual",   "Kigali", "Child Protection Hotline: +250 78 000 0002"),
            ("domestic", "Kigali", "Family Support Center: +250 78 000 0003"),
            ("trafficking","Kigali","Anti-Trafficking Unit: +250 78 000 0004"),
            ("general",  "Any",   "National Helpline: +250 78 000 0005")
        ]
        cur.executemany("INSERT INTO helplines (abuse_type, location, contact) VALUES (?,?,?)", defaults)
        conn.commit()

    conn.close()
