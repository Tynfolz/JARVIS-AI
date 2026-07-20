import sqlite3
import time


class MemoryDB:

    def __init__(self, db_path="jarvis_memory.db"):

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.conn.cursor()

        self._init_db()

    def _init_db(self):

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            key TEXT PRIMARY KEY,
            value TEXT,
            confidence REAL
        )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            text TEXT,
            timestamp REAL
        )
        """)

        self.conn.commit()

    # -------------------------
    # FACTS
    # -------------------------
    def set_fact(self, key, value, confidence=1.0):

        self.cur.execute("""
        INSERT OR REPLACE INTO facts (key, value, confidence)
        VALUES (?, ?, ?)
        """, (key, value, confidence))

        self.conn.commit()

    def get_fact(self, key):

        self.cur.execute("SELECT value FROM facts WHERE key=?", (key,))
        row = self.cur.fetchone()
        return row[0] if row else None

    def get_facts(self):

        self.cur.execute("SELECT key, value FROM facts")
        return dict(self.cur.fetchall())

    # -------------------------
    # MESSAGES
    # -------------------------
    def add_message(self, role, text):

        # защита от list/dict (ВАЖНО!)
        if isinstance(text, (list, dict)):
            text = str(text)

        self.cur.execute("""
        INSERT INTO messages (role, text, timestamp)
        VALUES (?, ?, ?)
        """, (role, text, time.time()))

        self.conn.commit()

    def get_last_messages(self, limit=10):

        self.cur.execute("""
        SELECT role, text FROM messages
        ORDER BY timestamp DESC
        LIMIT ?
        """, (limit,))

        rows = self.cur.fetchall()

        return list(reversed(rows))

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------