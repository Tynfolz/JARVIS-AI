import atexit
import faulthandler
import os
import sys
import threading
import time
import traceback
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
os.chdir(BASE)
if BASE not in sys.path:
    sys.path.insert(0, BASE)

# -------------------------
# НАСТРОЙКИ ДИАГНОСТИКИ
# -------------------------
USE_TRAY = "--no-tray" not in sys.argv
USE_GREETING = "--no-greet" not in sys.argv
HIDE_CONSOLE = False
SESSION_TIMEOUT = 30

# -------------------------
# ЛОГ
# -------------------------
_log = open(os.path.join(BASE, "jarvis.log"), "w", encoding="utf-8", buffering=1)
faulthandler.enable(_log, all_threads=True)


class Tee:
    def __init__(self, *streams):
        self.streams = [s for s in streams if s]

    def write(self, data):
        for s in self.streams:
            try:
                s.write(data)
                s.flush()
            except Exception:
                pass

    def flush(self):
        for s in self.streams:
            try:
                s.flush()
            except Exception:
                pass

    def isatty(self):
        return False


sys.stdout = Tee(sys.__stdout__, _log)
sys.stderr = Tee(sys.__stderr__, _log)


def _thread_error(args):
    name = args.thread.name if args.thread else "?"
    print(f"\n===== THREAD ERROR ({name}) =====")
    traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback)


threading.excepthook = _thread_error


@atexit.register
def _on_exit():
    print("👋 PROCESS EXIT")


def fatal(title):
    print(f"\n========== {title} ==========\n")
    traceback.print_exc()
    try:
        input("\nНажмите Enter...")
    except Exception:
        time.sleep(30)
    sys.exit(1)


def step(name):
    print(f"▶ {name}")


# -------------------------
# ИМПОРТЫ
# -------------------------
try:
    from core.jarvis_router import JarvisRouter
    from core.phrases import GREETINGS, LISTENING, random_phrase
    from speech.vosk_engine import VoskEngine
    from speech.wake_word import WakeWord
    from voice.voice_async import speak_async
except Exception:
    fatal("IMPORT ERROR")


def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return random_phrase(GREETINGS["morning"])
    if 12 <= hour < 18:
        return random_phrase(GREETINGS["day"])
    if 18 <= hour < 23:
        return random_phrase(GREETINGS["evening"])
    return random_phrase(GREETINGS["night"])


def run_tray():
    try:
        from tray.tray import start_tray
        start_tray(HIDE_CONSOLE)
    except Exception:
        print("\n===== TRAY ERROR =====")
        traceback.print_exc()


def main():
    print("Jarvis starting...")
    wake = None

    try:
        step("1 Vosk")
        engine = VoskEngine()
        step("2 Rustpotter")
        wake = WakeWord()
        atexit.register(wake.stop)
        step("3 Router")
        router = JarvisRouter()
    except Exception:
        if wake:
            wake.stop()
        fatal("STARTUP ERROR")

    if USE_TRAY:
        step("4 Tray")
        threading.Thread(target=run_tray, daemon=True, name="tray").start()
        time.sleep(1.5)
        step("4 Tray OK")

    if USE_GREETING:
        step("5 Greeting")
        speak_async(get_greeting())
        time.sleep(3)
        step("5 Greeting OK")

    print("🚀 JARVIS STARTED")

    session_active = False
    last_active = 0.0

    while True:
        try:
            if not session_active:
                if wake.listen():
                    print("🔥 WAKE WORD")
                    session_active = True
                    last_active = time.time()
                    router.sleep_requested = False
                    engine.reset()
                    time.sleep(0.5)
                    speak_async(random_phrase(LISTENING))
                continue

            if time.time() - last_active > SESSION_TIMEOUT:
                print("💤 SESSION CLOSED")
                session_active = False
                router.reset_context()
                continue

            text = engine.get_text()
            if not text:
                time.sleep(0.05)
                continue

            print("HEARD:", text)
            router.process(text)
            last_active = time.time()

            if router.sleep_requested:
                print("💤 SLEEP")
                router.sleep_requested = False
                session_active = False
                router.reset_context()
                engine.reset()

        except KeyboardInterrupt:
            break
        except Exception:
            print("\n========== MAIN LOOP ERROR ==========\n")
            traceback.print_exc()
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException:
        fatal("FATAL ERROR")