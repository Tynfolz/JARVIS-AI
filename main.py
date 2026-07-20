import sys
import os
import time
import threading
import traceback
import subprocess
import requests

# -------------------------
# FIX FOR EXE MODE
# -------------------------
if getattr(sys, "frozen", False):
    import io
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

print("1")

# -------------------------
# IMPORTS
# -------------------------
from speech.vosk_engine import VoskEngine
print("2")

from core.hybrid_router import HybridRouter
print("3")

from voice.voice_async import speak_async
print("4")

from tray.tray import start_tray
print("5")

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

    print("6 - CREATE VOSK")
    engine = VoskEngine()

    print("7 - CREATE ROUTER")
    router = HybridRouter()

    print("8 - SPEAK")
    speak_async("Приветствую, Сэр")

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

        text = engine.get_text()

        if not text:
            time.sleep(0.05)
            continue

        text = text.lower().strip()

        print("HEARD:", text)

        if "джарвис" in text:
            session_active = True
            last_active = time.time()

            router.listen_mode = "ACTIVE" 

            print("🔥 WAKE WORD")

            speak_async("Слушаю")

            continue

        if session_active:

            print("ROUTER:", text)

            result = router.process(text)

            if result == "SLEEP":

                session_active = False

                print("💤 SESSION CLOSED")

                continue

            last_active = time.time()

        time.sleep(0.01)


    except Exception:

        print("\n========== MAIN LOOP ERROR ==========\n")

        traceback.print_exc()

        input("\nНажмите Enter...")

        break

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------