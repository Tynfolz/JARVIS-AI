import os
import glob
import string


class AppSearch:

    def __init__(self):
        self.folders = self._get_search_folders()

    def _get_drives(self):
        """Get all available drives on Windows."""
        import ctypes
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            try:
                if os.path.exists(drive):
                    # Быстрая проверка, что диск реально читается (не съёмный без носителя)
                    if ctypes.windll.kernel32.GetDriveTypeW(drive) in (2, 3):
                        drives.append(drive)
            except Exception:
                continue
        return drives

    def _get_search_folders(self):
        """Build list of folders to search across all drives."""
        folders = []

        # User-specific folders (typically on C:)
        user_folders = [
            os.path.expandvars(r"%USERPROFILE%\Desktop"),
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
        ]

        # System folders (typically on C:)
        system_folders = [
            os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%ProgramFiles%"),
            os.path.expandvars(r"%ProgramFiles(x86)%"),
        ]

        # Add user folders if they exist
        for folder in user_folders:
            if os.path.exists(folder):
                folders.append(folder)

        # Add system folders if they exist
        for folder in system_folders:
            if os.path.exists(folder):
                folders.append(folder)

        # Search common program folders on ALL drives
        # Use a set to avoid duplicates
        seen_folders = set(folders)
        drives = self._get_drives()
        common_program_folders = [
            "Program Files",
            "Program Files (x86)",
            "Programs",
            "Apps",
            "Applications",
            "Games",
            "Steam",
            "SteamLibrary",
            "Epic Games",
            "GOG Galaxy",
            "Ubisoft",
            "Origin Games",
            "Battle.net",
        ]

        for drive in drives:
            for folder_name in common_program_folders:
                path = os.path.join(drive, folder_name)
                if os.path.exists(path) and path not in seen_folders:
                    folders.append(path)
                    seen_folders.add(path)

        # Also search root of each drive for portable apps (limit depth to avoid scanning entire drives)
        for drive in drives:
            # Check for portable apps in root
            portable_folders = ["PortableApps", "Portable", "Tools", "Bin", "Apps"]
            for pf in portable_folders:
                path = os.path.join(drive, pf)
                if os.path.exists(path) and path not in seen_folders:
                    folders.append(path)
                    seen_folders.add(path)

        return folders

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
                pattern = os.path.join(folder, "**", ext)

                try:
                    for path in glob.glob(pattern, recursive=True):
                        # Skip uninstallers and system files
                        if self._should_skip(path):
                            continue

                        apps.append({
                            "name": os.path.splitext(os.path.basename(path))[0],
                            "path": path,
                            "type": os.path.splitext(path)[1][1:].lower()
                        })
                except Exception as e:
                    print(f"SCAN ERROR in {folder}: {e}")

        return apps

    def _should_skip(self, path):
        """Filter out unwanted files."""
        path_lower = path.lower()
        # Check for uninstall/install related names in filename only
        filename = os.path.basename(path_lower)
        skip_name_patterns = [
            "uninstall",
            "unins",
            "setup",
            "install",
            "update",
            "updater",
            "crash",
            "report",
            "diagnostic",
            "repair",
            "unwise",
            "uninst",
        ]
        if any(pattern in filename for pattern in skip_name_patterns):
            return True

        # Check for system directories in path
        # Only skip 'windows' if it's at the root level (C:\Windows, D:\Windows, etc.)
        # Not if it's a subdirectory like AppData\Roaming\Microsoft\Windows\...
        path_parts = path_lower.replace('/', '\\').split('\\')

        # Check for system directories that should only match at specific positions
        # system32, syswow64, winsxs are always under Windows
        for i, part in enumerate(path_parts):
            if part in ('system32', 'syswow64', 'winsxs'):
                return True
            # 'windows' at position 1 (after drive letter) = C:\Windows
            if part == 'windows' and i == 1:
                return True

        # Check for multi-part system paths
        joined = '\\'.join(path_parts)
        if r'\appdata\local\temp\\' in joined or r'\appdata\local\microsoft\windowsapps\\' in joined:
            return True

        return False

    # -------------------------
    # SEARCH
    # -------------------------

    def search(self, query):
        query = query.lower()
        result = []

        for app in self.scan():
            if query in app["name"].lower():
                result.append(app)

        return result