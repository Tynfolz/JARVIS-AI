import os
import sqlite3
import threading
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "memory.db")


class MemoryDB:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.lock = threading.Lock()
        self.create_tables()

    def _exec(self, sql, params=(), fetch=False):
        with self.lock:
            cur = self.conn.execute(sql, params)
            rows = cur.fetchall() if fetch else None
            self.conn.commit()
            return rows

    def create_tables(self):
        self._exec("""CREATE TABLE IF NOT EXISTS conversations(
            id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, role TEXT, message TEXT)""")
        self._exec("""CREATE TABLE IF NOT EXISTS facts(
            id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, key TEXT UNIQUE,
            value TEXT, importance INTEGER DEFAULT 5, time TEXT)""")
        self._exec("""CREATE TABLE IF NOT EXISTS memory_processed(
            conversation_id INTEGER PRIMARY KEY)""")

    # история
    def add_message(self, role, message):
        self._exec(
            "INSERT INTO conversations(time, role, message) VALUES(?,?,?)",
            (str(datetime.now()), role, message),
        )

    def get_history(self, limit=50):
        """Последние сообщения, от новых к старым."""
        return self._exec(
            "SELECT role, message FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,), fetch=True,
        )

    # факты
    def add_fact(self, category, key, value, importance=5):
        self._exec(
            """INSERT INTO facts(category, key, value, importance, time) VALUES(?,?,?,?,?)
               ON CONFLICT(key) DO UPDATE SET value=excluded.value,
               importance=excluded.importance, time=excluded.time""",
            (category, key, value, importance, str(datetime.now())),
        )

    def get_facts(self):
        rows = self._exec("SELECT key, value FROM facts ORDER BY importance DESC", fetch=True)
        return {k: v for k, v in rows}

    def delete_fact(self, key):
        self._exec("DELETE FROM facts WHERE key=?", (key,))

    def clear_memory(self):
        self._exec("DELETE FROM facts")

    # сортировщик
    def get_unsorted_messages(self, limit=30):
        return self._exec(
            """SELECT id, role, message FROM conversations
               WHERE id NOT IN (SELECT conversation_id FROM memory_processed)
               ORDER BY id LIMIT ?""",
            (limit,), fetch=True,
        )

    def mark_processed(self, ids):
        with self.lock:
            self.conn.executemany(
                "INSERT OR IGNORE INTO memory_processed VALUES(?)", [(i,) for i in ids]
            )
            self.conn.commit()

    def cleanup_conversations(self, keep=5000):
        self._exec(
            """DELETE FROM conversations WHERE id NOT IN
               (SELECT id FROM conversations ORDER BY id DESC LIMIT ?)""",
            (keep,),
        )
        self._exec(
            "DELETE FROM memory_processed WHERE conversation_id NOT IN (SELECT id FROM conversations)"
        )