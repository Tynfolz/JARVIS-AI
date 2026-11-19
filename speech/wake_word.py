"""Wake-word «джарвис» на базе rustpotter-cli.

Что изменено по сравнению с прежней версией:
  * stdout rustpotter-cli читается отдельным потоком ВСЕГДА (раньше - только
    пока ждали wake-word, а во время сессии трубa не читалась и копились
    «старые» срабатывания, которые будили Джарвиса сразу после сна);
  * одно произнесённое слово может дать несколько строк (6 моделей) -
    дубли отсекаются (COOLDOWN), устаревшие события отбрасываются (MAX_AGE);
  * если rustpotter-cli упал - он перезапускается сам, а не «умирает» навсегда;
  * вывод читается как UTF-8 (убраны «РњРёРєСЂРѕС„РѕРЅ»);
  * осиротевшие rustpotter-cli.exe (после os._exit в трее/рестарте) убиваются
    при старте;
  * пороги и доп. флаги берутся из core/config.py (см. WAKE_* ниже),
    значения по умолчанию подходят, если в config.py ничего не добавлять.

Необязательные настройки для core/config.py:
    WAKE_THRESHOLD = 0.5        # ниже - чувствительнее (и больше ложных)
    WAKE_MIN_SCORES = 5
    WAKE_EAGER = True
    WAKE_EXTRA_ARGS = []        # например ["--gain-normalizer", "--band-pass"]
                                # точные имена флагов: rustpotter-cli spot --help
    WAKE_MODELS = None          # список имён .rpw; None = список по умолчанию
    WAKE_KILL_STALE = True

    WAKE_EXE = None             # путь к rustpotter-cli.exe.
                                # Относительный путь считается от корня проекта.
                                # None — авто-поиск (см. _find_rustpotter_exe).

Свои модели с именем jarvis-custom*.rpw в models/rustpotter подхватываются сами.

Поиск rustpotter-cli.exe (в порядке приоритета):
    1. config.WAKE_EXE (относительный путь — от корня проекта)
    2. models/rustpotter/rustpotter-cli.exe
    3. Корень проекта (рядом с main.py)
    4. PATH (через shutil.which)
Если нигде не найден — понятная ошибка при старте.
"""

import os
import queue
import shutil
import subprocess
import threading
import time
import weakref
from pathlib import Path

from core import config

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

DETECTION_MARK = "Wakeword detection"

_instances = weakref.WeakSet()

# Кеш найденного пути к rustpotter-cli.exe
_EXE_PATH = None


def _cfg(name, default):
    return getattr(config, name, default)


def _find_rustpotter_exe() -> str:
    """Ищет исполняемый файл rustpotter-cli.

    Порядок приоритета:
      1. config.WAKE_EXE — явно заданный путь (относительный считается от BASE)
      2. models/rustpotter/rustpotter-cli.exe
      3. BASE/rustpotter-cli.exe (рядом с main.py)
      4. PATH
    Возвращает строку с путём. Бросает FileNotFoundError, если нигде нет.
    """
    global _EXE_PATH
    if _EXE_PATH is not None:
        return _EXE_PATH

    # 1. Явно указан в config (относительный путь — от корня проекта)
    explicit = _cfg("WAKE_EXE", None)
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = BASE / p
        if p.is_file():
            _EXE_PATH = str(p)
            print(f"🔧 rustpotter-cli.exe (из config.WAKE_EXE): {_EXE_PATH}")
            return _EXE_PATH
        print(f"⚠️ config.WAKE_EXE={explicit} — файл не существует, ищу дальше")

    # 2. models/rustpotter/rustpotter-cli.exe
    local_models = MODELS_DIR / "rustpotter-cli.exe"
    if local_models.is_file():
        _EXE_PATH = str(local_models)
        print(f"🔧 rustpotter-cli.exe: {_EXE_PATH}")
        return _EXE_PATH

    # 3. Рядом с main.py
    local_root = BASE / "rustpotter-cli.exe"
    if local_root.is_file():
        _EXE_PATH = str(local_root)
        print(f"🔧 rustpotter-cli.exe: {_EXE_PATH}")
        return _EXE_PATH

    # 4. PATH
    found = shutil.which("rustpotter-cli")
    if found:
        _EXE_PATH = found
        print(f"🔧 rustpotter-cli.exe (из PATH): {_EXE_PATH}")
        return _EXE_PATH

    # Не нашли
    raise FileNotFoundError(
        "rustpotter-cli.exe не найден.\n"
        "Скачай бинарник для Windows (x86_64-pc-windows-msvc):\n"
        "  https://github.com/GiviMAD/rustpotter-cli/releases\n"
        f"и положи его в одно из мест:\n"
        f"  - {MODELS_DIR / 'rustpotter-cli.exe'}\n"
        f"  - {BASE / 'rustpotter-cli.exe'}\n"
        f"  - либо добавь папку с ним в PATH\n"
        f"Также можно указать путь явно в core/config.py:\n"
        f"  WAKE_EXE = r'models\\rustpotter\\rustpotter-cli.exe'"
    )


def _kill_stale():
    """Убивает осиротевшие rustpotter-cli.exe от прошлых запусков."""
    if os.name != "nt":
        return
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "rustpotter-cli.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=5,
        )
    except Exception:
        pass


def stop_all():
    """Остановить все rustpotter-cli. Звать перед os._exit(), там atexit не работает."""
    for w in list(_instances):
        w.stop()


class WakeWord:
    COOLDOWN = 2.0         # сек: повторные срабатывания после первого игнорируются
    MAX_AGE = 1.5          # сек: событие старше этого пришло «не вовремя» и игнорируется
    RESTART_EVERY = 3.0    # сек: не чаще одного перезапуска rustpotter-cli

    def __init__(self):
        # Сначала ищем .exe — до моделей, чтобы ошибка была по делу
        self.exe = _find_rustpotter_exe()

        self.models = self._find_models()

        print("Модели Rustpotter:")
        for model in self.models:
            print(" -", model.name)

        self._events = queue.Queue()
        self._last_fire = float("-inf")
        self._last_start = 0.0
        self._stopping = False
        self.process = None

        _instances.add(self)

        if _cfg("WAKE_KILL_STALE", True):
            _kill_stale()

        self._start()

    # ------------------------------------------------------------------
    # запуск
    # ------------------------------------------------------------------

    @staticmethod
    def _find_models():
        names = _cfg("WAKE_MODELS", None) or MODEL_NAMES
        models = [MODELS_DIR / name for name in names]

        missing = [str(m) for m in models if not m.is_file()]
        if missing:
            raise FileNotFoundError(
                "Не найдены модели Rustpotter:\n" + "\n".join(missing)
            )

        for custom in sorted(MODELS_DIR.glob("jarvis-custom*.rpw")):
            if custom not in models:
                models.append(custom)

        return models

    def _command(self):
        cmd = [
            self.exe, "spot",
            "-t", str(_cfg("WAKE_THRESHOLD", 0.5)),
            "-m", str(_cfg("WAKE_MIN_SCORES", 5)),
        ]
        if _cfg("WAKE_EAGER", True):
            cmd.append("-e")
        cmd += [str(arg) for arg in _cfg("WAKE_EXTRA_ARGS", [])]
        cmd += [str(model) for model in self.models]
        return cmd

    def _start(self):
        self._last_start = time.monotonic()
        cmd = self._command()
        print("Rustpotter cmd:", " ".join(cmd[:-len(self.models)]), "<models>")

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        threading.Thread(
            target=self._reader,
            args=(self.process,),
            daemon=True,
            name="rustpotter-reader",
        ).start()
        print("🟢 Rustpotter запущен")

    def _reader(self, proc):
        """Читает вывод rustpotter-cli постоянно, чтобы труба не забивалась."""
        try:
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                print("Rustpotter:", line)
                if DETECTION_MARK in line:
                    self._events.put(time.monotonic())
        except Exception as e:
            print("Rustpotter reader error:", e)

    def _ensure_alive(self):
        if self._stopping or self.process is None:
            return
        code = self.process.poll()
        if code is None:
            return
        if time.monotonic() - self._last_start < self.RESTART_EVERY:
            return
        print(f"⚠️ rustpotter-cli завершился (код {code}), перезапускаю...")
        self._start()

    # ------------------------------------------------------------------
    # API (совместим со старым: listen() -> bool)
    # ------------------------------------------------------------------

    def listen(self, timeout=0.5):
        """True, если только что прозвучало wake-word. Ждёт не дольше timeout секунд."""
        end = time.monotonic() + timeout

        while True:
            left = max(end - time.monotonic(), 0.0)
            try:
                ts = self._events.get(timeout=left)
            except queue.Empty:
                self._ensure_alive()
                return False

            if time.monotonic() - ts > self.MAX_AGE:
                continue    # сработало, пока шла сессия - не наше
            if ts - self._last_fire < self.COOLDOWN:
                continue    # дубль от соседней модели
            self._last_fire = ts
            return True

    def clear(self):
        """Выбросить накопленные события (звать при закрытии сессии)."""
        try:
            while True:
                self._events.get_nowait()
        except queue.Empty:
            pass

    def stop(self):
        self._stopping = True
        proc = self.process
        if proc is None or proc.poll() is not None:
            return

        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()