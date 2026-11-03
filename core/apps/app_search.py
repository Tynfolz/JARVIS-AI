import os
import glob


class AppSearch:

    def __init__(self):

        self.folders = [

            # Рабочий стол
            os.path.expandvars(
                r"%USERPROFILE%\Desktop"
            ),

            # Меню Пуск
            os.path.expandvars(
                r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
            ),

            os.path.expandvars(
                r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"
            ),

            # Program Files
            os.path.expandvars(
                r"%ProgramFiles%"
            ),

            os.path.expandvars(
                r"%ProgramFiles(x86)%"
            ),

            # Local Programs
            os.path.expandvars(
                r"%LOCALAPPDATA%\Programs"
            ),

        ]


    # -------------------------
    # SCAN
    # -------------------------

    def scan(self):

        apps = []

        exts = (

            "*.lnk",
            "*.exe"

        )

        for folder in self.folders:

            if not os.path.exists(folder):
                continue

            for ext in exts:

                pattern = os.path.join(
                    folder,
                    "**",
                    ext
                )

                for path in glob.glob(
                    pattern,
                    recursive=True
                ):

                    apps.append({

                        "name": os.path.splitext(
                            os.path.basename(path)
                        )[0],

                        "path": path,

                        "type": os.path.splitext(path)[1][1:].lower()

                    })

        return apps


    # -------------------------
    # SEARCH
    # -------------------------

    def search(
            self,
            query
    ):

        query = query.lower()

        result = []

        for app in self.scan():

            if query in app["name"].lower():

                result.append(app)

        return result