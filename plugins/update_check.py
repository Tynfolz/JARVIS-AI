from core.updater import JarvisUpdater

PRIORITY = 30
TRIGGERS = ("проверь обновлени", "проверить обновлени", "есть обновлени")


def match(text):
    return any(t in text for t in TRIGGERS)


def run(jarvis, text):
    update = JarvisUpdater().check()
    if not update:
        jarvis.say("Обновлений нет")
        return True

    jarvis.state["last_update"] = update
    print("UPDATE AVAILABLE:", update["version"])
    print("FILES:", update["files"])
    print("CHANGELOG:", update["changelog"])

    jarvis.say(f"Доступно обновление версии {update['version']}. Скажите: установи обновление.")
    return True