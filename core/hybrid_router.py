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
from ai.memory_sorter import MemorySorter

class HybridRouter:

    def __init__(self):
        print("🔥 INIT START SkillEngine")
        self.sleep_requested = False
        self.skills = SkillEngine()
        self.piper = PiperSettingsRouter()
        self.weather = WeatherRouter()
        self.currency = CurrencyRouter()
        self.search = SearchService()
        self.modes = ModeManager()
        self.weather_settings = WeatherSettingsRouter()
        self.piper = PiperSettingsRouter()
        self.last_action = None
        self.db = MemoryDB()

        self.memory_sorter = MemorySorter(
            self.db
        )

        self.message_counter = 0

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
        # SIMPLE MEMORY DETECT
        # -------------------------

        memory_patterns = {

            "люблю игру": "game",
            "моя любимая игра": "game",

            "люблю музыку": "music",
            "мой любимый фильм": "movie",

            "я играю в": "game",

        }

        for phrase, key in memory_patterns.items():

            if phrase in text:

                value = text.replace(
                    phrase,
                    ""
                ).strip()

                if value:
                    self.db.add_fact(
                        "user",
                        key,
                        value,
                        8
                    )

                    print(
                        "🧠 FACT SAVED:",
                        key,
                        value
                    )

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
        # MEMORY CHECK
        # -------------------------

        facts = self.db.get_facts()

        memory_context = "\n".join(
            [
                f"{k}: {v}"
                for k, v in facts.items()
            ]
        )


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

        Используй память пользователя.

        Если в памяти есть ответ на вопрос —
        используй её.

        Не придумывай факты.
        Если информации нет в памяти — скажи, что не знаешь.
        Не заменяй неизвестные данные догадками.


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

        # -------------------------
        # MEMORY SORT
        # -------------------------

        self.message_counter += 1

        if self.message_counter >= 20:

            try:

                self.memory_sorter.analyze()

            except Exception as e:

                print(
                    "MEMORY SORT ERROR:",
                    e
                )

            self.message_counter = 0

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------