import sqlite3
import os
from datetime import datetime


BASE = os.path.dirname(
    os.path.dirname(__file__)
)


DB_PATH = os.path.join(
    BASE,
    "memory.db"
)


class MemoryDB:


    def __init__(self):

        self.conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

        self.create_tables()



    def create_tables(self):

        cursor = self.conn.cursor()


        # -------------------------
        # ИСТОРИЯ ДИАЛОГОВ
        # -------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT,

            role TEXT,

            message TEXT

        )
        """)



        # -------------------------
        # ПАМЯТЬ
        # -------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT,

            key TEXT UNIQUE,

            value TEXT,

            importance INTEGER DEFAULT 5,

            time TEXT

        )
        """)



        # -------------------------
        # ОБРАБОТАННЫЕ СООБЩЕНИЯ
        # -------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_processed(

            conversation_id INTEGER PRIMARY KEY

        )
        """)



        self.conn.commit()



    # -------------------------
    # СОХРАНЕНИЕ СООБЩЕНИЯ
    # -------------------------

    def add_message(
        self,
        role,
        message
    ):

        cursor = self.conn.cursor()


        cursor.execute(
            """
            INSERT INTO conversations
            (
                time,
                role,
                message
            )
            VALUES(?,?,?)
            """,
            (
                str(datetime.now()),
                role,
                message
            )
        )


        self.conn.commit()



    # -------------------------
    # ИСТОРИЯ
    # -------------------------

    def get_history(
        self,
        limit=50
    ):

        cursor = self.conn.cursor()


        cursor.execute(
            """
            SELECT role,message

            FROM conversations

            ORDER BY id DESC

            LIMIT ?
            """,
            (limit,)
        )


        return cursor.fetchall()



    # -------------------------
    # ДОБАВИТЬ ФАКТ
    # -------------------------

    def add_fact(
        self,
        category,
        key,
        value,
        importance=5
    ):

        cursor = self.conn.cursor()


        cursor.execute(
            """
            INSERT INTO facts
            (
                category,
                key,
                value,
                importance,
                time
            )

            VALUES(?,?,?,?,?)


            ON CONFLICT(key)

            DO UPDATE SET

                value=excluded.value,

                importance=excluded.importance,

                time=excluded.time

            """,
            (
                category,
                key,
                value,
                importance,
                str(datetime.now())
            )
        )


        self.conn.commit()



    # -------------------------
    # ПОЛУЧИТЬ ПАМЯТЬ
    # -------------------------

    def get_facts(self):

        cursor = self.conn.cursor()


        cursor.execute(
            """
            SELECT

                category,
                key,
                value

            FROM facts

            ORDER BY importance DESC

            """
        )


        result = {}


        for category, key, value in cursor.fetchall():

            result[key] = value


        return result



    # -------------------------
    # УДАЛИТЬ ФАКТ
    # -------------------------

    def delete_fact(
        self,
        key
    ):

        cursor = self.conn.cursor()


        cursor.execute(
            """
            DELETE FROM facts

            WHERE key=?

            """,
            (key,)
        )


        self.conn.commit()



    # -------------------------
    # ОЧИСТИТЬ ПАМЯТЬ
    # -------------------------

    def clear_memory(self):

        cursor = self.conn.cursor()


        cursor.execute(
            """
            DELETE FROM facts
            """
        )


        self.conn.commit()



    # -------------------------
    # НЕОБРАБОТАННЫЕ СООБЩЕНИЯ
    # -------------------------

    def get_unsorted_messages(
        self,
        limit=30
    ):

        cursor = self.conn.cursor()


        cursor.execute(
            """
            SELECT

                id,
                role,
                message

            FROM conversations

            WHERE id NOT IN

            (

                SELECT conversation_id

                FROM memory_processed

            )

            ORDER BY id

            LIMIT ?

            """,
            (limit,)
        )


        return cursor.fetchall()



    # -------------------------
    # ПОМЕТИТЬ КАК ОБРАБОТАННЫЕ
    # -------------------------

    def mark_processed(
        self,
        ids
    ):

        cursor = self.conn.cursor()


        for i in ids:

            cursor.execute(
                """
                INSERT OR IGNORE INTO memory_processed

                VALUES(?)

                """,
                (i,)
            )


        self.conn.commit()

    # -------------------------
    # AUTO CLEANUP
    # -------------------------

    def cleanup_conversations(
            self,
            keep=5000
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM conversations

            WHERE id NOT IN
            (
                SELECT id

                FROM conversations

                ORDER BY id DESC

                LIMIT ?
            )
            """,
            (keep,)
        )

        self.conn.commit()