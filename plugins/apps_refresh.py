TRIGGERS = (
    "обнови приложения", "обновить приложения",
    "обнови программы", "обновить программы", "обнови программу",
)


def match(text):
    return any(t in text for t in TRIGGERS)


def run(jarvis, text):
    jarvis.say("Сканирую приложения, это может занять время")
    count = jarvis.apps.refresh()
    jarvis.say(f"База приложений обновлена. Найдено {count} программ")
    return True