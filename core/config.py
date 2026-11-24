import os
import re

MICROPHONE_NAME = "Razer Barracuda X 2.4"

# PIPER
PIPER_VOICE = "ruslan"
PIPER_LENGTH_SCALE = 0.83      # скорость (меньше = быстрее)
PIPER_NOISE_SCALE = 0.50       # эмоциональность
PIPER_NOISE_W = 0.70           # четкость

# WEATHER
WEATHER_CITY = "Москва"

# PLUGINS
PLUGIN_MATCH_THRESHOLD = 65    # 0..100 — ниже = более нечёткое совпадение (фразы не нужно говорить буква в букву)
ENABLE_PLUGINS = True
# LLM
LLM_DEVICE = "cpu"             # "cpu" — процессор, "gpu" — видеокарта
LLM_GPU_LAYERS = -1            # сколько слоёв на видеокарту (-1 = все; если мало VRAM — 20..30)
LLM_THREADS = 0                # потоки CPU (0 = авто)
LLM_CTX = 4096                 # размер контекста
LLM_PRELOAD = False            # грузить модель при старте (True) или при первом вопросе (False)
MEMORY_SORT_EVERY = 20         # анализ памяти раз в N сообщений

#====================================================================================================================================================================================

# ===== WAKE WORD ENGINE SELECTION =====
# porcupine — рекомендуемый (точный, быстрый, промышленный стандарт)
# vosk — использует уже загруженную модель Vosk (не требует ключа)
# rustpotter — текущий движок на 6 моделях
# pocketsphinx – простой офлайн‑детектор (может лагать на некоторых микрофонах)
WAKE_ENGINE = "vosk" # "porcupine" | "vosk" | "rustpotter" | "pocketsphinx"

# Porcupine (Picovoice) — https://console.picovoice.ai/
PORCUPINE_ACCESS_KEY = ""        # Вставьте ваш AccessKey здесь
PORCUPINE_SENSITIVITY = 0.6      # 0.0-1.0, выше = чувствительнее
PORCUPINE_KEYWORDS = ("jarvis",) # Ключевые слова (built-in: "jarvis", "alexa", "hey google", и др.)

# Vosk wake-word
VOSK_WAKE_KEYWORDS = ("джарвис",)
VOSK_WAKE_THRESHOLD = 0.5

# ----- POCKETSPHINX SETTINGS -----
# (Опционально) Ключевое слово и порог чувствительности для PocketSphinx.
# Если вы не планируете использовать этот движок, оставьте их без изменения.
POCKETSPHINX_KEYWORD = "jarvis"
POCKETSPHINX_THRESHOLD = 1e-10

WAKE_THRESHOLD = 0.6  # ниже - чувствительнее (и больше ложных)
WAKE_MIN_SCORES = 5
WAKE_EAGER = True
WAKE_EXTRA_ARGS = []  # например ["--gain-normalizer", "--band-pass"]
# точные имена флагов: rustpotter-cli spot --help
WAKE_MODELS = None  # список имён .rpw; None = список по умолчанию
WAKE_KILL_STALE = True
WAKE_EXE = r"models\rustpotter\rustpotter-cli.exe"

# Доп. настройки фильтрации (подбираются автоматически, можно переопределить):
WAKE_MIN_GAIN = 0.3          # --min-gain  для gain-normalizer
WAKE_MAX_GAIN = 2.5          # --max-gain
WAKE_LOW_CUTOFF = 80         # --low-cutoff (band-pass нижний)
WAKE_HIGH_CUTOFF = 4000      # --high-cutoff (band-pass верхний)


def set_config(name, value):
    """Меняет настройку в памяти и сохраняет в этот файл."""
    globals()[name] = value

    path = os.path.abspath(__file__)
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    new_line = f"{name} = {value!r}"
    data, count = re.subn(
        rf"^{re.escape(name)}\s*=[^#\n]*", lambda m: new_line + " ", data, count=1, flags=re.M
    )
    if count == 0:
        data += f"\n{new_line}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

    print(f"💾 CONFIG SAVED: {name} = {value!r}")