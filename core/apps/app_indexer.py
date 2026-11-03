from core.apps.app_search import AppSearch
from core.apps.app_database import AppDatabase


class AppIndexer:


    def __init__(self):

        self.search = AppSearch()

        self.db = AppDatabase()



    # -------------------------
    # REFRESH
    # -------------------------

    def refresh(self):

        print(
            "📦 SCANNING APPLICATIONS..."
        )


        apps = self.search.scan()


        print(
            "FOUND:",
            len(apps)
        )


        self.db.clear()


        count = 0


        for app in apps:

            try:

                self.db.add(

                    app["name"],

                    app["path"],

                    app["type"]

                )

                count += 1


            except Exception as e:

                print(
                    "APP ADD ERROR:",
                    e
                )


        print(
            f"✅ APPLICATION INDEX UPDATED: {count}"
        )


        return count

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------