import sqlite3

DB_NAME = "users.db"


def connect():
    return sqlite3.connect(DB_NAME)


def crate_table():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            lat REAL,
            lon REAL
        )
        """)


def add_user(tg_id, full_name, phone, lat, lon):
    with connect() as con:
        con.execute("""
        INSERT OR REPLACE INTO users 
        (tg_id, full_name, phone, lat, lon)
        VALUES (?, ?, ?, ?, ?)
        """, (tg_id, full_name, phone, lat, lon))


def get_user(tg_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("""
        SELECT * FROM users WHERE tg_id = ?
        """, (tg_id,))
        return cur.fetchone()


def update_name(tg_id, full_name):
    with connect() as con:
        con.execute("UPDATE users SET full_name=? WHERE tg_id=?",
                    (full_name, tg_id))


def update_phone(tg_id, phone):
    with connect() as con:
        con.execute("UPDATE users SET phone=? WHERE tg_id=?",
                    (phone, tg_id))
