from core.file_updater import FileUpdater
from core.restart import restart_jarvis

PRIORITY = 30
TRIGGERS = (
    "установи обновление", "установить обновление", "обновись",
    "обнови джарвис", "обновить джарвис", "примени обновление", "поставь обновление",
)


def match(text):
    return any(t in text for t in TRIGGERS)


def run(jarvis, text):
    update = jarvis.state.get("last_update")
    if not update:
        jarvis.say("Сначала проверьте обновления, сэр")
        return True

    files = [f for f in update.get("files", []) if isinstance(f, str)]
    if not files:
        jarvis.say("В обновлении нет файлов")
        return True

    jarvis.say("Начинаю обновление")
    print("🔄 UPDATE START", update.get("version"), files)

    count = FileUpdater().update_files(files)
    if count != len(files):
        print(f"❌ UPDATE FAILED: {count}/{len(files)}")
        jarvis.say("Обновление не завершено. Перезапуска не будет.")
        return True

    jarvis.state["last_update"] = None
    jarvis.say("Обновление завершено. Перезапускаюсь.")
    restart_jarvis()
    return True