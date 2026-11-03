import sqlite3
import os


BASE = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

DB_PATH = os.path.join(
    BASE,
    "apps.db"
)


class AppDatabase:

    def __init__(self):

        self.conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

        self.create()


    # -------------------------
    # CREATE
    # -------------------------

    def create(self):

        cursor = self.conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS apps(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            path TEXT UNIQUE,

            type TEXT,

            last_used TEXT

        )

        """)

        self.conn.commit()


    # -------------------------
    # CLEAR
    # -------------------------

    def clear(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "DELETE FROM apps"
        )

        self.conn.commit()


    # -------------------------
    # ADD
    # -------------------------

    def add(

            self,

            name,

            path,

            app_type

    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """

            INSERT OR IGNORE INTO apps(

                name,

                path,

                type

            )

            VALUES(?,?,?)

            """,

            (

                name,

                path,

                app_type

            )

        )

        self.conn.commit()


    # -------------------------
    # FIND
    # -------------------------

    def find(

            self,

            query

    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """

            SELECT

                name,

                path,

                type

            FROM apps

            WHERE lower(name)

            LIKE ?

            LIMIT 1

            """,

            (

                f"%{query.lower()}%",

            )

        )

        return cursor.fetchone()


    # -------------------------
    # LIST
    # -------------------------

    def list(self):

        cursor = self.conn.cursor()

        cursor.execute(

            """

            SELECT name

            FROM apps

            ORDER BY name

            """

        )

        return [

            x[0]

            for x in cursor.fetchall()

        ]