import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE / "models" / "rustpotter"

MODEL_NAMES = [
    "jarvis-community-1.rpw",
    "jarvis-community-2.rpw",
    "jarvis-community-3.rpw",
    "jarvis-community-4.rpw",
    "jarvis-community-5.rpw",
    "jarvis-default.rpw",
]


class WakeWord:
    def __init__(self):
        models = [MODELS_DIR / name for name in MODEL_NAMES]
        missing = [str(model) for model in models if not model.is_file()]
        if missing:
            raise FileNotFoundError(
                "Не найдены модели Rustpotter:\n" + "\n".join(missing)
            )

        print("Модели Rustpotter:")
        for model in models:
            print(" -", model.name)

        self.process = subprocess.Popen(
            [
                "rustpotter-cli", "spot",
                "-t", "0.65",
                "-m", "5",
                "-e",
                *(str(model) for model in models),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        print("🟢 Rustpotter запущен")

    def listen(self):
        line = self.process.stdout.readline()

        if not line:
            raise RuntimeError(
                f"rustpotter-cli завершился (код {self.process.wait()})"
            )

        # Показываем сообщения Rustpotter, чтобы не потерять причину ошибки.
        print("Rustpotter:", line.rstrip())
        return "Wakeword detection" in line

    def stop(self):
        if self.process.poll() is not None:
            return

        self.process.terminate()
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()