PHRASES = [
    "открой телеграм",
    "запусти телеграм",
    "открой telegram",
    "телеграм"
]


def run(jarvis, text):
    # Try to find Telegram in the app database first
    app = jarvis.apps.db.find("telegram")
    if app:
        name, path, app_type = app
        if app_type == "lnk":
            import os
            os.startfile(path)
        else:
            import subprocess
            subprocess.Popen(path)
        jarvis.say("Открываю Telegram")
        return True

    # Fallback: try running via shell (if in PATH)
    try:
        import subprocess
        subprocess.Popen("telegram", shell=True)
        jarvis.say("Открываю Telegram")
        return True
    except Exception:
        jarvis.say("Telegram не найден. Скажите «обнови приложения»")
        return False