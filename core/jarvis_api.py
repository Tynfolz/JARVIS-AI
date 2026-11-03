import os
import subprocess
import webbrowser

import pyperclip

from core.apps.apps_api import AppsAPI
from core.phrases import COMMAND_DONE, random_phrase
from voice.tts import speak
from voice.voice_async import speak_async


class OpenAPI:
    def program(self, command):
        try:
            subprocess.Popen(command)
            return True
        except Exception as e:
            print("OPEN PROGRAM ERROR:", e)
            return False

    def file(self, path):
        try:
            os.startfile(path)
            return True
        except Exception as e:
            print("OPEN FILE ERROR:", e)
            return False

    def url(self, url):
        webbrowser.open(url)
        return True


class ClipboardAPI:
    def copy(self, text):
        pyperclip.copy(text)

    def paste(self):
        return pyperclip.paste()


class ContextAPI:
    def __init__(self, router):
        self._ctx = router.context

    def set(self, **kwargs):
        for key, value in kwargs.items():
            self._ctx.set(key, value)

    def get(self, key):
        return self._ctx.get(key)


class MemoryAPI:
    def __init__(self, router):
        self._db = router.db

    def add(self, category, key, value, importance=5):
        self._db.add_fact(category, key, value, importance)

    def facts(self):
        return self._db.get_facts()

    def get(self, key, default=None):
        return self._db.get_facts().get(key, default)

    def forget(self, key):
        self._db.delete_fact(key)


class ConfigAPI:
    def get(self, key, default=None):
        from core import config
        return getattr(config, key, default)

    def set(self, key, value):
        from core import config
        config.set_config(key, value)


class AIAPI:
    def ask(self, prompt, rules=None, temperature=0.3, max_tokens=300):
        from ai import llm
        system = llm.JARVIS_PROMPT
        if rules:
            system += "\n\nЗАДАЧА:\n" + rules
        return llm.complete(prompt, system=system, temperature=temperature, max_tokens=max_tokens)

    def search(self, query, max_results=5):
        from ai.search import web_search
        return web_search(query, max_results=max_results)


class PluginsAPI:
    def __init__(self, router):
        self._router = router

    def reload(self):
        self._router.plugin_loader.load()

    def list(self):
        return [p.PLUGIN_NAME for p in self._router.plugin_loader.plugins]


class JarvisAPI:
    """Через этот объект плагины общаются с ядром."""

    def __init__(self, router):
        self.open = OpenAPI()
        self.apps = AppsAPI()
        self.clipboard = ClipboardAPI()
        self.context = ContextAPI(router)
        self.memory = MemoryAPI(router)
        self.config = ConfigAPI()
        self.ai = AIAPI()
        self.plugins = PluginsAPI(router)
        self.state = {}

    def say(self, text):
        speak(text)

    def say_async(self, text):
        speak_async(text)

    def done(self):
        speak_async(random_phrase(COMMAND_DONE))