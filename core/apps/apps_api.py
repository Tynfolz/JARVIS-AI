import os
import subprocess

from core.apps.app_database import AppDatabase


class AppsAPI:

    def __init__(self):
        self.db = AppDatabase()

    def open(self, name):
        app = self.db.find(name)
        if not app:
            return False

        app_name, path, app_type = app
        try:
            if app_type == "lnk":
                os.startfile(path)
            else:
                subprocess.Popen(path)
            print("🚀 OPEN:", app_name)
            return True
        except Exception as e:
            print("APP OPEN ERROR:", e)
            return False

    def refresh(self):
        from core.apps.app_indexer import AppIndexer
        return AppIndexer().refresh()

    def list(self):
        return self.db.list()