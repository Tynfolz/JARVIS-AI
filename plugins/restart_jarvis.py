import os
import sys
import time
import subprocess


PHRASES = [
    "перезапусти себя",
    "перезапусти джарвис",
    "перезапусти джарвиса",
    "перезапусти jarvis",
    "перезагрузка джарвис",
    "перезагрузка джарвиса",
    "перезагрузись",
    "перезагрузи себя",
    "рестарт",
    "сделай рестарт",
    "рестарт джарвис",
    "рестарт джарвиса",
    "restart",
    "restart jarvis",
]


def _find_main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base, "main.py"),
        os.path.join(base, "jarvis.py"),
        os.path.join(base, "run.py"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path, base
    return None, base


def run(jarvis, text):
    main_path, base = _find_main()

    if not main_path:
        jarvis.say("Не нашёл main.py для перезапуска")
        return True

    jarvis.say("Перезапускаюсь")

    # Дать TTS договорить
    time.sleep(1.2)

    python = sys.executable
    creationflags = 0

    # Без консольного окна-призрака на Windows
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    try:
        subprocess.Popen(
            [python, main_path],
            cwd=base,
            creationflags=creationflags,
            close_fds=True,
        )
    except Exception as e:
        print("RESTART ERROR:", e)
        jarvis.say("Не удалось перезапуститься")
        return True

    # Закрыть текущий процесс
    try:
        os._exit(0)
    except Exception:
        sys.exit(0)