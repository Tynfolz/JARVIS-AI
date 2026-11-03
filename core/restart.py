import os
import sys
import time
import subprocess


def restart_jarvis(delay=0.5):
    """
    Запускает новый экземпляр JARVIS
    с теми же аргументами командной строки
    и завершает текущий процесс.
    """

    try:

        python_executable = sys.executable

        script_path = os.path.abspath(
            sys.argv[0]
        )

        arguments = sys.argv[1:]

        print("===================================")
        print("🔄 JARVIS RESTART")
        print("PYTHON:", python_executable)
        print("SCRIPT:", script_path)
        print("ARGS:", arguments)
        print("===================================")

        time.sleep(delay)

        subprocess.Popen(
            [
                python_executable,
                script_path,
                *arguments
            ],
            cwd=os.path.dirname(script_path),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        print("🚀 NEW JARVIS PROCESS STARTED")

        # Завершаем старый процесс
        os._exit(0)

    except Exception as e:

        print(
            "❌ RESTART ERROR:",
            e
        )

        return False

    return True
