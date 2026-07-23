import sys
import os
import time
import threading
import traceback
import subprocess
import requests
from core.phrases import random_phrase
from voice.voice_async import speak_async
from core.phrases import LISTENING
from core.phrases import GREETINGS
from datetime import datetime
from speech.vosk_engine import VoskEngine
from speech.wake_word import WakeWord
from core.hybrid_router import HybridRouter
from voice.voice_async import speak_async
from tray.tray import start_tray


# -------------------------
# FIX FOR EXE MODE
# -------------------------
if getattr(sys, "frozen", False):
    import io
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

# -------------------------
# START TRAY
# -------------------------
threading.Thread(
    target=start_tray,
    daemon=True
).start()

print("Jarvis starting...")

# -------------------------
# INIT
# -------------------------
try:

    engine = VoskEngine()
    wake = WakeWord()
    router = HybridRouter()

    def get_greeting():

        hour = datetime.now().hour

        if 5 <= hour < 12:
            return random_phrase(GREETINGS["morning"])

        elif 12 <= hour < 18:
            return random_phrase(GREETINGS["day"])

        elif 18 <= hour < 23:
            return random_phrase(GREETINGS["evening"])

        else:
            return random_phrase(GREETINGS["night"])


    speak_async(get_greeting())

    print("🚀 JARVIS STARTED")

except Exception:

    print("\n========== STARTUP ERROR ==========\n")
    traceback.print_exc()

    input("\nНажмите Enter...")

    sys.exit()

# -------------------------
# DIALOG MODE
# -------------------------
session_active = False
last_active = 0

SESSION_TIMEOUT = 30

# -------------------------
# MAIN LOOP
# -------------------------
while True:

    try:

        if session_active:

            if time.time() - last_active > SESSION_TIMEOUT:

                session_active = False
                last_active = 0

                print("💤 SESSION CLOSED")

                if hasattr(router, "reset_context"):
                    router.reset_context()

                router.skills.reset()

        # -------------------------
        # Ждем только wakeword
        # -------------------------

        if not session_active:

            if wake.listen():
                session_active = True
                last_active = time.time()

                print("🔥 WAKE WORD")

                router.listen_mode = "ACTIVE"
                router.sleep_requested = False

                engine.reset()

                time.sleep(0.5)

                speak_async(random_phrase(LISTENING))

                continue

        # -------------------------
        # После пробуждения слушаем команду
        # -------------------------

        if engine is None:
            continue

        text = engine.get_text()

        if router.sleep_requested:
            print("💤 ROUTER REQUEST SLEEP")

            router.sleep_requested = False

            session_active = False
            last_active = 0

            engine.reset()

            continue

        if not text:
            continue

        print("HEARD:", text)

        if text:
            result = router.process(text)

            last_active = time.time()

    except Exception:

        print("\n========== MAIN LOOP ERROR ==========\n")

        traceback.print_exc()

        input("\nНажмите Enter...")

        break

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------