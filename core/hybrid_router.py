from ai.ai_hybrid import ask_ai
from voice.tts import speak
from ai.memory_db import MemoryDB
from voice.voice_async import speak_async
from core.skill_engine import SkillEngine
from ai.search import web_search
from core.phrases import MODES, random_phrase
from core.phrases import SEARCH_NOT_FOUND
from core.phrases import COMMAND_NOT_FOUND
from core import config
from core.router.modes import ModeManager
from api.currency import get_currency
from core.router.weather_router import WeatherRouter
from core.router.currency_router import CurrencyRouter
from core.router.search_router import SearchService
from core.router.piper_settings_router import PiperSettingsRouter
from core.router.weather_settings_router import WeatherSettingsRouter

class HybridRouter:

    def __init__(self):
        print("🔥 INIT START SkillEngine")
        self.sleep_requested = False
        self.db = MemoryDB()
        self.skills = SkillEngine()
        self.piper = PiperSettingsRouter()
        self.weather = WeatherRouter()
        self.currency = CurrencyRouter()
        self.search = SearchService()
        self.modes = ModeManager()
        self.weather_settings = WeatherSettingsRouter()
        self.piper = PiperSettingsRouter()
        self.last_action = None

        print("🚀 JARVIS FINAL ROUTER READY")

    def process(self, text: str):

        if not text:
            return

        text = text.lower().strip()

        print("ROUTER:", text)

        mode = self.modes.process(text)

        if mode == "sleep":
            self.sleep_requested = True

            return True

        if mode:
            return True


        # -------------------------
        # MEMORY
        # -------------------------
        self.db.add_message("user", text)

        self.last_action = text

        # -------------------------
        # core/router
        # -------------------------

        if self.weather.process(text):
            return

        if self.currency.process(text):
            return

        if self.search.process(text):
            return

        if self.piper.process(text):
            return True

        if self.weather_settings.process(text):
            return True
        # -------------------------
        # SKILLS
        # -------------------------

        result = self.skills.process(text)

        if result:
            return


        # -------------------------
        # AI DISABLED
        # -------------------------
        if not self.modes.ai_mode:
            speak_async(random_phrase(COMMAND_NOT_FOUND), ),

            return

        # -------------------------
        # AI
        # -------------------------
        facts = self.db.get_facts()

        memory_context = "\n".join(
            [f"{k}: {v}" for k, v in facts.items()]
        )

        prompt = f"""
    Ты JARVIS — русский AI ассистент.

    ВАЖНО:
    - отвечай только на русском
    - будь кратким

    ПАМЯТЬ:
    {memory_context}

    Последняя команда:
    {self.last_action}

    Пользователь:
    {text}
    """

        try:

            response = ask_ai(prompt)

        except Exception:

            response = "Ошибка AI"

        print("AI:", response)

        self.db.add_message("jarvis", response)

        speak(response)

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------