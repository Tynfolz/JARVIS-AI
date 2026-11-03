import ast
import urllib.request

from core.version import VERSION


class JarvisUpdater:

    def __init__(self):
        self.manifest_url = (
            "https://raw.githubusercontent.com/"
            "Tynfolz/JARVIS-AI/main/update_manifest.py"
        )

    # -------------------------
    # LOAD MANIFEST
    # -------------------------

    def get_manifest(self):

        try:
            with urllib.request.urlopen(
                self.manifest_url,
                timeout=10
            ) as response:

                data = response.read().decode("utf-8")

            tree = ast.parse(data)

            manifest = {}

            for node in tree.body:

                if not isinstance(node, ast.Assign):
                    continue

                for target in node.targets:

                    if not isinstance(target, ast.Name):
                        continue

                    try:
                        manifest[target.id] = ast.literal_eval(
                            node.value
                        )

                    except (ValueError, TypeError):
                        pass

            return manifest

        except Exception as e:

            print(
                "MANIFEST ERROR:",
                e
            )

            return None

    # -------------------------
    # CHECK
    # -------------------------

    def check(self):

        manifest = self.get_manifest()

        if not manifest:
            return False

        remote_version = manifest.get("VERSION")

        if not remote_version:
            print("MANIFEST: VERSION NOT FOUND")
            return False

        print(
            "LOCAL VERSION:",
            VERSION
        )

        print(
            "REMOTE VERSION:",
            remote_version
        )

        if remote_version != VERSION:

            return {
                "version": remote_version,
                "files": manifest.get("FILES", []),
                "changelog": manifest.get("CHANGELOG", [])
            }

        return False