import os
import shutil
import urllib.request


class FileUpdater:

    def __init__(self):

        self.github_raw = (
            "https://raw.githubusercontent.com/"
            "Tynfolz/JARVIS-AI/main/"
        )

        self.base = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

    # -------------------------
    # DOWNLOAD ONE FILE
    # -------------------------

    def download_file(self, relative_path):

        relative_path = relative_path.replace("\\", "/")

        url = self.github_raw + relative_path

        local = os.path.join(
            self.base,
            relative_path.replace("/", os.sep)
        )

        directory = os.path.dirname(local)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        backup = local + ".bak"

        try:

            # -------------------------
            # BACKUP
            # -------------------------

            if os.path.exists(local):

                shutil.copy2(
                    local,
                    backup
                )

            # -------------------------
            # DOWNLOAD
            # -------------------------

            print(
                "DOWNLOADING:",
                url
            )

            with urllib.request.urlopen(
                url,
                timeout=20
            ) as response:

                data = response.read()

            # -------------------------
            # WRITE
            # -------------------------

            temporary = local + ".update"

            with open(
                temporary,
                "wb"
            ) as file:

                file.write(data)

            # -------------------------
            # REPLACE
            # -------------------------

            os.replace(
                temporary,
                local
            )

            # -------------------------
            # REMOVE BACKUP
            # -------------------------

            if os.path.exists(backup):
                os.remove(backup)

            print(
                "UPDATED:",
                relative_path
            )

            return True

        except Exception as e:

            print(
                "UPDATE ERROR:",
                relative_path,
                e
            )

            # remove temporary file

            temporary = local + ".update"

            if os.path.exists(temporary):

                try:
                    os.remove(temporary)
                except Exception:
                    pass

            # restore backup

            if os.path.exists(backup):

                try:

                    shutil.move(
                        backup,
                        local
                    )

                    print(
                        "BACKUP RESTORED:",
                        relative_path
                    )

                except Exception as restore_error:

                    print(
                        "BACKUP RESTORE ERROR:",
                        restore_error
                    )

            return False

    # -------------------------
    # UPDATE FILES
    # -------------------------

    def update_files(self, files):

        if not files:
            print("NO FILES TO UPDATE")
            return 0

        updated = 0

        for file in files:

            if not isinstance(file, str):
                continue

            if self.download_file(file):
                updated += 1

        return updated