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
PLUGIN_MATCH_THRESHOLD = 80    # 0..100

# LLM
LLM_DEVICE = "gpu"             # "cpu" — процессор, "gpu" — видеокарта
LLM_GPU_LAYERS = -1            # сколько слоёв на видеокарту (-1 = все; если мало VRAM — 20..30)
LLM_THREADS = 0                # потоки CPU (0 = авто)
LLM_CTX = 4096                 # размер контекста
LLM_PRELOAD = False            # грузить модель при старте (True) или при первом вопросе (False)
MEMORY_SORT_EVERY = 20         # анализ памяти раз в N сообщений


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