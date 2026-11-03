import threading

from ai import llm
from ai.memory_db import MemoryDB
from ai.memory_sorter import MemorySorter
from core import config
from core.context_manager import ContextManager
from core.jarvis_api import JarvisAPI
from core.modes import ModeManager
from core.phrases import COMMAND_NOT_FOUND, random_phrase
from core.plugin_loader import PluginLoader
from voice.tts import speak
from voice.voice_async import speak_async

MEMORY_PATTERNS = [
    ("моя любимая игра", "game"),
    ("люблю игру", "game"),
    ("я играю в", "game"),
    ("люблю музыку", "music"),
    ("мой любимый фильм", "movie"),
]


class JarvisRouter:

    def __init__(self):
        self.sleep_requested = False

        self.db = MemoryDB()
        self.memory_sorter = MemorySorter(self.db)
        self.context = ContextManager()
        self.modes = ModeManager()
        self.plugin_loader = PluginLoader()
        self.jarvis = JarvisAPI(self)

        self._messages_since_sort = 0
        self._sort_lock = threading.Lock()

        if getattr(config, "LLM_PRELOAD", False):
            threading.Thread(target=llm.preload, daemon=True).start()

        print(f"🚀 JARVIS ROUTER READY ({len(self.plugin_loader.plugins)} plugins)")

    def reset_context(self):
        self.context.clear()
        self.modes.reset()
        for plugin in self.plugin_loader.plugins:
            reset = getattr(plugin, "reset", None)
            if callable(reset):
                try:
                    reset()
                except Exception as e:
                    print(f"RESET ERROR {plugin.PLUGIN_NAME}:", e)

    def process(self, text):
        if not text:
            return False

        text = text.lower().strip()
        print("ROUTER:", text)

        # 1. режимы
        mode = self.modes.process(text)
        if mode == "sleep":
            self.sleep_requested = True
            return True
        if mode:
            return True

        # 2. память
        self.db.add_message("user", text)
        self._detect_facts(text)
        self._maybe_sort_memory()

        # 3. плагины
        if self.plugin_loader.process(self.jarvis, text):
            return True

        # 4. ИИ
        if not self.modes.ai_mode:
            speak_async(random_phrase(COMMAND_NOT_FOUND))
            return False

        self._answer_with_ai(text)
        return True

    def _answer_with_ai(self, text):
        facts = self.db.get_facts()
        memory_context = "\n".join(f"{k}: {v}" for k, v in facts.items())
        history = list(reversed(self.db.get_history(limit=7)))[:-1]

        response = llm.ask_ai(text, memory_context=memory_context, history=history)
        print("AI:", response)

        self.db.add_message("jarvis", response)
        speak(response)

    def _detect_facts(self, text):
        for phrase, key in MEMORY_PATTERNS:
            if phrase in text:
                value = text.split(phrase, 1)[1].strip()
                if value:
                    self.db.add_fact("user", key, value, 8)
                    print("🧠 FACT SAVED:", key, value)

    def _maybe_sort_memory(self):
        self._messages_since_sort += 1
        if self._messages_since_sort < config.MEMORY_SORT_EVERY:
            return
        if not self._sort_lock.acquire(blocking=False):
            return

        self._messages_since_sort = 0

        def worker():
            try:
                self.memory_sorter.analyze()
            except Exception as e:
                print("MEMORY SORT ERROR:", e)
            finally:
                self._sort_lock.release()

        threading.Thread(target=worker, daemon=True).start()