import ast
import importlib
import importlib.util
import os
import re
import subprocess
import sys
import traceback

from rapidfuzz import fuzz

from core import config

# Слова, которые выкидываем перед матчингом (можно сказать «джарвис, пожалуйста, включи музыку»)
STOP_WORDS = {
    "джарвис", "джарвиз", "ярвис", "gerd", "jarvis",
    "пожалуйста", "пожалуй", "будь", "добр", "добрый",
    "кажи", "скажи", "сделай", "сделай", "выполни", "выполняй",
    "хочу", "хотелось", "бы", "побудь", "если", "не", "сложно",
    "мне", "мою", "мой", "мои", "тебя", "ты", "вы", "ваш", "ваша",
    "алиса", "маруся", "саша", "ассистент", "робот", "бот",
}

# Регулярки для нормализации: множественные пробелы, знаки препинания
_CLEAN_RE = re.compile(r"[^\w\s-]+")
_MULTI_SPACE_RE = re.compile(r"\s+")


def _normalize_text(text: str) -> str:
    """Удаляет стоп-слова и нормализует пробелы/пунктуацию."""
    text = text.lower().strip()
    text = _CLEAN_RE.sub(" ", text)
    words = [w for w in text.split() if w not in STOP_WORDS]
    return _MULTI_SPACE_RE.sub(" ", " ".join(words)).strip()



PLUGINS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugins"
)

# pip-имя → имя модуля
IMPORT_NAMES = {
    "pywin32": "win32api",
    "pillow": "PIL",
    "pyyaml": "yaml",
    "beautifulsoup4": "bs4",
}


def phrase_score(text, phrase):
    phrase = phrase.lower().strip()
    if not phrase:
        return 0
    if text == phrase:
        return 100
    score = fuzz.token_sort_ratio(text, phrase)
    return max(score, fuzz.token_set_ratio(text, phrase) * 0.9)


def best_phrase(text, phrases):
    best, best_score = None, 0
    norm_text = _normalize_text(text)
    for p in phrases:
        s = phrase_score(norm_text, p)
        if s > best_score:
            best, best_score = p, s
    return best, best_score


class PluginLoader:

    def __init__(self):
        self.plugins = []
        self._checked_deps = set()
        # Если плагины отключены, пропускаем их загрузку – ускоряем старт
        if config.ENABLE_PLUGINS:
            self.load()
        else:
            print("⚙️ Плагины отключены (ENABLE_PLUGINS=False)")
    def install_dependencies(self, deps):
        for dep in deps:
            if dep in self._checked_deps:
                continue
            self._checked_deps.add(dep)

            base = re.split(r"[<>=!\[ ]", dep)[0]
            module = IMPORT_NAMES.get(base.lower(), base.replace("-", "_"))
            if importlib.util.find_spec(module) is not None:
                continue

            print(f"📦 Installing dependency: {dep}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                importlib.invalidate_caches()
            except Exception as e:
                print(f"❌ INSTALL ERROR {dep}:", e)

    def get_requirements(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if getattr(target, "id", "") == "REQUIREMENTS":
                            return list(ast.literal_eval(node.value))
        except Exception as e:
            print("REQUIREMENTS ERROR:", path, e)
        return []

    def load(self):
        plugins = []

        if not os.path.isdir(PLUGINS_DIR):
            print("❌ PLUGINS DIR NOT FOUND:", PLUGINS_DIR)
            self.plugins = plugins
            return

        for file in sorted(os.listdir(PLUGINS_DIR)):
            if not file.endswith(".py") or file.startswith("_"):
                continue

            name = file[:-3]
            path = os.path.join(PLUGINS_DIR, file)

            try:
                reqs = self.get_requirements(path)
                if reqs:
                    self.install_dependencies(reqs)

                spec = importlib.util.spec_from_file_location(f"jarvis_plugin_{name}", path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if not callable(getattr(module, "run", None)):
                    continue
                if not hasattr(module, "PHRASES") and not callable(getattr(module, "match", None)):
                    continue

                module.PLUGIN_NAME = name
                plugins.append(module)
                print(f"🔌 Loaded plugin: {name}")

            except Exception:
                print(f"❌ PLUGIN ERROR {name}:")
                traceback.print_exc()

        self.plugins = plugins

    def score(self, plugin, text):
        match = getattr(plugin, "match", None)
        if callable(match):
            try:
                result = match(text)
            except Exception as e:
                print(f"MATCH ERROR {plugin.PLUGIN_NAME}:", e)
                return 0
            return 100 if result is True else float(result or 0)

        return best_phrase(text, getattr(plugin, "PHRASES", []))[1]

    def process(self, jarvis, text):
        # Нормализуем один раз и используем везде
        norm_text = _normalize_text(text)
        threshold = getattr(config, "PLUGIN_MATCH_THRESHOLD", 80)

        candidates = []
        for plugin in self.plugins:
            s = self.score(plugin, norm_text)
            if s >= threshold:
                candidates.append((s, getattr(plugin, "PRIORITY", 0), plugin))

        candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)

        for s, _, plugin in candidates:
            print(f"🔌 TRY {plugin.PLUGIN_NAME} ({s:.0f})")
            try:
                result = plugin.run(jarvis, text)
            except Exception:
                print(f"❌ PLUGIN RUN ERROR {plugin.PLUGIN_NAME}:")
                traceback.print_exc()
                jarvis.say("Ошибка в плагине")
                return True

            if result is False:
                continue
            return True

        return False